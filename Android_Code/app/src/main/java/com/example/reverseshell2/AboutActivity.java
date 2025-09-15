package com.example.reverseshell2;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import java.util.Random;

/**
 * Fake About activity for evasion - appears legitimate to static analysis
 */
public class AboutActivity extends Activity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Create a simple legitimate-looking about page
        TextView textView = new TextView(this);
        textView.setText("System Optimizer v2.1.3\n\n" +
                "© 2024 TechSoft Solutions\n" +
                "All rights reserved.\n\n" +
                "This application helps optimize your device performance " +
                "by managing background processes and system resources.\n\n" +
                "For support, visit: www.techsoft-solutions.com");
        textView.setPadding(40, 40, 40, 40);
        textView.setTextSize(14);
        
        setContentView(textView);
        
        // Simulate legitimate app behavior
        simulateLegitimateActivity();
    }
    
    private void simulateLegitimateActivity() {
        new Thread(() -> {
            try {
                // Random delay to appear like real user interaction
                Thread.sleep(new Random().nextInt(2000) + 1000);
                
                // Simulate some legitimate operations
                System.gc();
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
    }
    
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        finish();
    }
}