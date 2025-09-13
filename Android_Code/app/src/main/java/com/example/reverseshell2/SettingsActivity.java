package com.example.reverseshell2;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.os.Handler;
import android.os.Looper;
import java.util.Random;

/**
 * Legitimate-looking settings activity for detection evasion
 */
public class SettingsActivity extends AppCompatActivity {
    
    private TextView statusText;
    private Handler handler;
    private Random random;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Create simple UI to look legitimate
        TextView textView = new TextView(this);
        textView.setText("App Settings\n\nSynchronization: Enabled\nBackground Updates: On\nNotifications: Enabled");
        textView.setPadding(50, 100, 50, 50);
        textView.setTextSize(16);
        setContentView(textView);
        
        statusText = textView;
        handler = new Handler(Looper.getMainLooper());
        random = new Random();
        
        // Start legitimate-looking background activity
        startPeriodicUpdates();
    }
    
    private void startPeriodicUpdates() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                // Simulate app activity to avoid suspicion
                updateStatus();
                handler.postDelayed(this, 30000 + random.nextInt(60000)); // 30-90 seconds
            }
        }, 5000);
    }
    
    private void updateStatus() {
        String[] statuses = {
            "Checking for updates...",
            "Syncing data...",
            "Processing notifications...",
            "Optimizing performance..."
        };
        
        String currentText = statusText.getText().toString();
        String newStatus = statuses[random.nextInt(statuses.length)];
        statusText.setText(currentText + "\n\nStatus: " + newStatus);
        
        // Clear status after a few seconds
        handler.postDelayed(() -> {
            statusText.setText("App Settings\n\nSynchronization: Enabled\nBackground Updates: On\nNotifications: Enabled");
        }, 3000);
    }
}