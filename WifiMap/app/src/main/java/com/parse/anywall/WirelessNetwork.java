package com.parse.anywall;

import com.parse.ParseClassName;
import com.parse.ParseGeoPoint;
import com.parse.ParseObject;
import com.parse.ParseQuery;

/**
 * Data model for a Network.
 * Subclass
 */

@ParseClassName("Network")
public class WirelessNetwork extends ParseObject {

  public String getSsid() {
    return getString("ssid");
  }


  public String getBssid() {
    return getString("bssid");
  }


  public ParseGeoPoint getLocation() {
    return getParseGeoPoint("location");
  }


  public String getSecurity() {
    return getString("security");
  }

  public static ParseQuery<WirelessNetwork> getQuery() {
    return ParseQuery.getQuery(WirelessNetwork.class);
  }
}
