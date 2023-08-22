package com.appsnipp.modernlogin;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class ShowResults extends AppCompatActivity {

    private StringBuilder stringBuilder = new StringBuilder();
    private TextView mShowInput;
    private TextView mShowReport;

    private int[] timeArray;
    private String[] emotionArray;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_results);

        mShowInput = findViewById(R.id.show_output_text_view);
        mShowReport = findViewById(R.id.show_overall_report_text_view);

        getBackendData();

    }



    public void getBackendData(){

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

                final StringBuilder contentResult = new StringBuilder();

                String url = "http://192.168.8.100:5000/api/getData";

                try {
                    URL requestURL =new URL(url);
                    URLConnection connection =requestURL.openConnection();
                    BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));

                    String contentString ;

                    while ((contentString = br.readLine()) != null){
                        contentResult.append(contentString);
                    }

                    br.close();

                } catch (IOException e) {
                    e.printStackTrace();
                }


                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                        try {
                            convertToJson(contentResult.toString());
                            showReport();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                });
            }
        });
        thread.start();
    }

    public void convertToJson(String response) throws JSONException {

//        JSONObject data = new JSONObject(response);

        JSONArray jsonArray = new JSONArray(response);

        timeArray = new int[jsonArray.length()];
        emotionArray = new String[jsonArray.length()];

        for (int i = 0 ; i < jsonArray.length() ; i ++){
            JSONObject obj = (JSONObject) jsonArray.get(i);

            String timeFrame = obj.getString("TimeFrame");
            String emotion = obj.getString("Emotion");

            int timeTemp = obj.getInt("TimeFrame");
            String emotionTemp = obj.getString("Emotion");
            timeArray[i] = timeTemp;
            emotionArray[i] = emotionTemp;

            stringBuilder.append(timeFrame).append(" : ").append(emotion).append("\n");

        }

        System.out.println(stringBuilder.toString());

        String output = stringBuilder.toString();
        mShowInput.setText(output);

    }

    public void goBackButton(View view) {
        finish();
    }

    public void showReport(){

        StringBuilder builder = new StringBuilder("Overall Result : " + "\n");

        int totalTime = timeArray[timeArray.length-1];

        System.out.println(emotionArray[0]);

        int totalHappy = 0;
        int totalAngry = 0;
        int totalCalm = 0;
        int totalSurprised = 0;
        int totalDisgust = 0;

        for (int i = 0 ; i < emotionArray.length - 1 ; i ++){

            switch (emotionArray[i]) {
                case "happy":
                    totalHappy = totalHappy + 1;
                    break;
                case "angry":
                    totalAngry = totalAngry + 1;
                    break;
                case "calm":
                    totalCalm = totalCalm + 1;
                    break;
                case "surprised":
                    totalSurprised = totalSurprised + 1;
                    break;
                case "disgust":
                    totalDisgust = totalDisgust + 1;
                    break;
            }

        }

        System.out.println("ANGRY : " + totalAngry +  "   Happy : " + totalHappy + "  TIME " + totalTime);

        float percentageAngry =((float) totalAngry*3 / (float)totalTime )*(float)100;
        builder.append("Angry : ").append(percentageAngry).append(" %").append("\n");

        float percentageHappy =((float) totalHappy*3 / (float)totalTime )*(float)100;
        builder.append("Happy : ").append(percentageHappy).append(" %").append("\n");

        float percentageCalm =((float) totalCalm*3 / (float)totalTime )*(float)100;
        builder.append("Calm : ").append(percentageCalm).append(" %").append("\n");

        float percentageSurprised =((float) totalSurprised*3 /(float) totalTime )*(float)100;
        builder.append("Surprised : ").append(percentageSurprised).append(" %").append("\n");

        float percentageDisgust =((float) totalDisgust*3 / (float) totalTime ) * (float) 100;
        builder.append("Disgust : ").append(percentageDisgust).append(" %").append("\n");

        mShowReport.setText(builder.toString());


    }


    public void files(){

        String path = getApplicationContext().getFilesDir().getAbsolutePath();


    }
}