<?php

/**
 * Icinga Wordpress Plugin
 *
 * Put this into your Wordpress directory (where wp-load.php lives).
 *
 * @author Marcello Perathoner <marcello@perathoner.de>
 */

require_once 'wp-load.php';


/**
 * Explode a version string into an array of 3 integers.
 *
 * @function explode_version
 *
 * @param {string} ver - The version as string, eg. '4.8.2'.
 *
 * @returns {int[3]} The version as big-endian array of 3 integers.
 */

function explode_version ($ver)
{
    $res = array_map ('intval', explode ('.', $ver));
    $res[0] = isset ($res[0]) ? res [0] : 0;
    $res[1] = isset ($res[1]) ? res [1] : 0;
    $res[2] = isset ($res[2]) ? res [2] : 0;
    return $res;
}

global $wp_version;
$ver = explode_version ($wp_version);

wp_version_check ();
wp_update_plugins ();
wp_update_themes ();

$upd_status = 0;
$upd_cores = array ();
$upd_plugins = array ();
$upd_themes = array ();

foreach (get_site_transient ('update_core')->updates as $core_update) {
    $upd = explode_version ($core_update->current);
    if ($upd[0] > $ver[0] || $upd[1] > $ver[1] || $upd[2] > $ver[2]) {
        $upd_cores[$core_update->current] = true;
        $upd_status |= 0x04;
        if ($upd[0] == $ver[0] && $upd[1] == $ver[1]) {
            /* point release. probably a security upgrade. make it critical */
            $upd_status |= 0x08;
        }
    }
}

foreach (get_site_transient ('update_plugins')->response as $plugin_file => $plugin_data) {
    $upd_plugins[] = $plugin_file;
    $upd_status |= 0x02;
}

foreach (get_site_transient ('update_themes')->response as $stylesheet => $data) {
    $upd_themes[] = wp_get_theme ($stylesheet);
    $upd_status |= 0x01;
}


/* format the response */

$status = 'OK';
if ($upd_status & 0x07) {
    $status = 'WARNING';
}
if ($upd_status & 0x08) {
    $status = 'CRITICAL';
}

$what = array ();
if ($upd_status & 0x04) {
    $upd_cores = array_keys ($upd_cores);
    natsort ($upd_cores);
    $what[] = 'Core (' . implode ($upd_cores, ', ') . ')';
}
if ($upd_status & 0x02) {
    $what[] = count ($upd_plugins) . ' Plugin (' . implode ($upd_plugins, ', ') . ')';
}
if ($upd_status & 0x01) {
    $what[] = count ($upd_themes) . ' Theme (' . implode ($upd_themes, ', ') . ')';
}

$msg = '';
if ($upd_status) {
    $msg = ': ' . implode ($what, ' and ') . ' updates available';
}

echo "WORDPRESS $status - Version = $wp_version$msg";
