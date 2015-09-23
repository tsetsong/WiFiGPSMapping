package com.parse.anywall;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;



/**
 * Activity which starts an intent for app launcher (MainActivity)
 *
 */
public class DispatchActivity extends Activity {

  public DispatchActivity() {
  }

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
      startActivity(new Intent(this, MainActivity.class));

  }

}
