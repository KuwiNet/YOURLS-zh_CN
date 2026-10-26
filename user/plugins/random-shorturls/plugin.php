<?php
/*
Plugin Name: 随机短链接
Plugin URI: https://yourls.org/
Description: 为短链接分配随机关键字，如 bitly（sho.rt/hJudjK）
Version: 1.2.1
Author: Ozh
Author URI: https://ozh.org/
*/

/* Release History:
*
* 1.0 Initial release
* 1.1 Added: don't increment sequential keyword counter & save one SQL query
* Fixed: plugin now complies to character set defined in config.php
* 1.2 Adopted as YOURLS core plugin under a new name
* Now configured via YOURLS options instead of editing plugin file
* 1.2.1 Update HTML tag in notice
*/

// No direct call
if( !defined( 'YOURLS_ABSPATH' ) ) die();

// Only register things if the old third-party plugin is not present
if( function_exists('ozh_random_keyword') ) {
    yourls_add_notice( "<strong>随机短链接</strong> 插件无法运行，除非先移除 <strong>Random Keywords</strong> 插件。" );
} else {
    // filter registration happens conditionally, to avoid conflicts
    // settings action is left out here, as it allows checking settings before deleting the old plugin
    yourls_add_filter( 'random_keyword', 'ozh_random_shorturl' );
    yourls_add_filter( 'get_next_decimal', 'ozh_random_shorturl_next_decimal' );
}

// Generate a random keyword
function ozh_random_shorturl() {
    $possible = yourls_get_shorturl_charset() ;
    $str='';
    while( strlen( $str ) < yourls_get_option( 'random_shorturls_length', 5 ) ) {
        $str .= substr($possible, rand( 0, strlen( $possible ) - 1 ), 1 );
    }
    return $str;
}

// Don't increment sequential keyword tracker
function ozh_random_shorturl_next_decimal( $next ) {
    return ( $next - 1 );
}

// Plugin settings page etc.
yourls_add_action( 'plugins_loaded', 'ozh_random_shorturl_add_settings' );
function ozh_random_shorturl_add_settings() {
    yourls_register_plugin_page( 'random_shorturl_settings', '随机短链接设置', 'ozh_random_shorturl_settings_page' );
}

function ozh_random_shorturl_settings_page() {
    // Check if form was submitted
    if( isset( $_POST['random_length'] ) ) {
        // If so, verify nonce
        yourls_verify_nonce( 'random_shorturl_settings' );
        // and process submission if nonce is valid
        ozh_random_shorturl_settings_update();
    }

    $random_length = yourls_get_option('random_shorturls_length', 5);
    $nonce = yourls_create_nonce( 'random_shorturl_settings' );

    echo <<<HTML
        <main>
            <h2>随机短链接设置</h2>
            <form method="post">
            <input type="hidden" name="nonce" value="$nonce" />
            <p>
                <label>随机关键字长度</label>
                <input type="number" name="random_length" min="1" max="128" value="$random_length" />
            </p>
            <p><input type="submit" value="保存" class="button" /></p>
            </form>
        </main>
HTML;
}

function ozh_random_shorturl_settings_update() {
    $random_length = $_POST['random_length'];

    if( $random_length ) {
        if( is_numeric( $random_length ) ) {
            yourls_update_option( 'random_shorturls_length', intval( $random_length ) );
        } else {
            echo "错误：给出的长度不是数字。";
        }
    } else {
        echo "错误：未提供长度值。";
    }
}
