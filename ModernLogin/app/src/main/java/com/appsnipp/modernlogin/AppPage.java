package com.appsnipp.modernlogin;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;


import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;



public class AppPage extends AppCompatActivity {

    private ProgressBar mProgressBar;
    private TextView mLoadingText;

    private int mProgressStatus = 0;
    private Handler mHandler = new Handler();

    private static final String TAG = "AppPage";

    private StringBuilder stringBuilder = new StringBuilder();
    private TextView mShowInput;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_app_page);

        mProgressBar = (ProgressBar) findViewById (R.id.progressBar);
        mLoadingText = (TextView) findViewById(R.id.LoadingCompleteTextView);

        new Thread(new Runnable() {
            @Override
            public void run() {
                while (mProgressStatus < 100){
                    mProgressStatus++;
                    SystemClock.sleep(50);
                    mHandler.post(new Runnable() {
                        @Override
                        public void run() {
                            mProgressBar.setProgress(mProgressStatus);
                        }
                    });
                }
                mHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        mLoadingText.setVisibility(View.VISIBLE);
                    }
                });
            }
        });



        BottomNavigationView navView = findViewById(R.id.nav_view);
        Log.d(TAG, "onCreate: started.");

        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);
    }

    public void submitFile(View view){

        Intent intent = new Intent(this,ShowResults.class);
        startActivity(intent);

    }




}