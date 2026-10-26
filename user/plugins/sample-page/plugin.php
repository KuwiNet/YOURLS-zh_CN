<?php
/*
Plugin Name: 示例后台页面
Plugin URI: http://yourls.org/
Description: 一个用于保存用户自定义选项的插件后台页面示例
Version: 1.0
Author: Ozh
Author URI: http://ozh.org/
*/

// No direct call
if( !defined( 'YOURLS_ABSPATH' ) ) die();

// Register our plugin admin page
yourls_add_action( 'plugins_loaded', 'ozh_yourls_samplepage_add_page' );
function ozh_yourls_samplepage_add_page() {
    yourls_register_plugin_page( 'sample_page', '示例后台页面', 'ozh_yourls_samplepage_do_page' );
    // parameters: page slug, page title, and function that will display the page itself
}

// Display admin page
function ozh_yourls_samplepage_do_page() {

    // Check if a form was submitted
    if( isset( $_POST['test_option'] ) ) {
        // Check nonce
        yourls_verify_nonce( 'sample_page' );

        // Process form
        ozh_yourls_samplepage_update_option();
    }

    // Get value from database
    $test_option = yourls_get_option( 'test_option' );

    // Create nonce
    $nonce = yourls_create_nonce( 'sample_page' );

    echo <<<HTML
        <h2>示例插件后台管理页面</h2>
        <p>该插件在选项数据库中存储一个整数</p>
        <form method="post">
        <input type="hidden" name="nonce" value="$nonce" />
        <p><label for="test_option">请输入整数</label> <input type="text" id="test_option" name="test_option" value="$test_option" /></p>
        <p><input type="submit" value="更新值" /></p>
        </form>

HTML;
}

// Update option in database
function ozh_yourls_samplepage_update_option() {
    $in = $_POST['test_option'];

    if( $in ) {
        // Validate test_option. ALWAYS validate and sanitize user input.
        // Here, we want an integer
        $in = intval( $in);

        // Update value in database
        yourls_update_option( 'test_option', $in );
    }
}
