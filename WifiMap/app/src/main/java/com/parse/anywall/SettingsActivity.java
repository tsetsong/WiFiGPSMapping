package com.parse.anywall;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.RadioGroup.OnCheckedChangeListener;
import android.widget.Spinner;


import java.util.Collections;
import java.util.List;

/**
 * Activity that displays the settings screen.
 */
public class SettingsActivity extends Activity {
  public ProgressDialog pDialog;
  private List<Float> availableOptions = Application.getConfigHelper().getSearchDistanceAvailableOptions();

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_settings);

    final Spinner filterSpinner = (Spinner) findViewById(R.id.filter_spinner);
    // Create an ArrayAdapter using the string array  security _spinner and a default spinner layout
    ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array.security_spinner, android.R.layout.simple_spinner_item);
    // Specify the layout to use when the list of choices appears
    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
  filterSpinner.setAdapter(adapter);



    float currentSearchDistance = Application.getSearchDistance();
    if (!availableOptions.contains(currentSearchDistance)) {
      availableOptions.add(currentSearchDistance);
    }
    Collections.sort(availableOptions);

    // The search distance choices
    RadioGroup searchDistanceRadioGroup = (RadioGroup) findViewById(R.id.searchdistance_radiogroup);

    for (int index = 0; index < availableOptions.size(); index++) {
      float searchDistance = availableOptions.get(index);

      RadioButton button = new RadioButton(this);
      button.setId(index);
      button.setText(getString(R.string.settings_distance_format, (int)searchDistance));
      searchDistanceRadioGroup.addView(button, index);

      if (currentSearchDistance == searchDistance) {
        searchDistanceRadioGroup.check(index);
      }
    }

    // Set up the selection handler to save the selection to the application
    searchDistanceRadioGroup.setOnCheckedChangeListener(new OnCheckedChangeListener() {
      public void onCheckedChanged(RadioGroup group, int checkedId) {
        Application.setSearchDistance(availableOptions.get(checkedId));
      }
    });

    // Set up the refresh buton handler
    Button refresh = (Button) findViewById(R.id.refresh_button);
    refresh.setOnClickListener(new OnClickListener() {
      public void onClick(View v) {

        SharedPreferences sp=getSharedPreferences("FilterMode", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor=sp.edit();
        editor.putString("filter",filterSpinner.getSelectedItem().toString());
        editor.commit();
        //To check spinner data is been saved in SharedPreferences
        //Log.d("DEBUG", filterSpinner.getSelectedItem().toString()+ ":sp put string");
        // Start and intent for the dispatch activity
        Intent intent = new Intent(SettingsActivity.this, DispatchActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
      }
    });
  }

}
