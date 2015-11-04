package com.parse.anywall;

import android.content.Context;
import android.content.SharedPreferences;

import com.parse.Parse;
import com.parse.ParseCrashReporting;
import com.parse.ParseObject;

public class Application extends android.app.Application {
  // Debugging switch
  public static final boolean APPDEBUG = false;

  // Debugging tag for the application
  public static final String APPTAG = "WifiMap";

  // Key for saving the search distance preference
  private static final String KEY_SEARCH_DISTANCE = "searchDistance";

  private static final float DEFAULT_SEARCH_DISTANCE = 250.0f;

  private static SharedPreferences preferences;

  private static ConfigHelper configHelper;

  public Application() {
  }

  @Override
  public void onCreate() {
    super.onCreate();
    //register subclass WirelessNetwork data model
    ParseObject.registerSubclass(WirelessNetwork.class);
    //Setup Parse
    Parse.initialize(this, "HcbZRxgwdVIfIXdIgZKC4wRmitpOdSUZpgJbEUni", "YoL2ZyyhhZjoVNPD9JWMQ42cVxL8OtOR2FEGKCA4");

    preferences = getSharedPreferences("searchDistance", Context.MODE_PRIVATE);

    configHelper = new ConfigHelper();
    configHelper.fetchConfigIfNeeded();
  }

  public static float getSearchDistance() {
    return preferences.getFloat(KEY_SEARCH_DISTANCE, DEFAULT_SEARCH_DISTANCE);
  }

  public static ConfigHelper getConfigHelper() {
    return configHelper;
  }

  public static void setSearchDistance(float value) {
    preferences.edit().putFloat(KEY_SEARCH_DISTANCE, value).commit();
  }




}
