package com.example.reverseshell2;

import android.content.Context;
import android.util.Log;
import androidx.work.Constraints;
import androidx.work.Data;
import androidx.work.NetworkType;
import androidx.work.OneTimeWorkRequest;
import androidx.work.PeriodicWorkRequest;
import androidx.work.WorkManager;
import java.util.concurrent.TimeUnit;

/**
 * WorkManager scheduler for modern Android background task management
 * Handles all background work scheduling in compliance with Android restrictions
 */
public class WorkScheduler {
    
    private static final String TAG = "WorkScheduler";
    private static final String HEALTH_CHECK_WORK = "health_check_work";
    private static final String CONNECTIVITY_WORK = "connectivity_work";
    private static final String DATA_SYNC_WORK = "data_sync_work";
    
    /**
     * Schedule periodic health check work
     */
    public static void schedulePeriodicHealthCheck(Context context) {
        try {
            Constraints constraints = new Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(false)
                .build();
            
            Data inputData = new Data.Builder()
                .putString("work_type", "health_check")
                .build();
            
            PeriodicWorkRequest healthCheckRequest = new PeriodicWorkRequest.Builder(
                BackgroundWorker.class, 15, TimeUnit.MINUTES)
                .setConstraints(constraints)
                .setInputData(inputData)
                .addTag(HEALTH_CHECK_WORK)
                .build();
            
            WorkManager.getInstance(context)
                .enqueueUniquePeriodicWork(HEALTH_CHECK_WORK, 
                    androidx.work.ExistingPeriodicWorkPolicy.REPLACE, 
                    healthCheckRequest);
            
            Log.d(TAG, "Periodic health check scheduled");
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to schedule health check", e);
        }
    }
    
    /**
     * Schedule connectivity check work
     */
    public static void scheduleConnectivityCheck(Context context) {
        try {
            Constraints constraints = new Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build();
            
            Data inputData = new Data.Builder()
                .putString("work_type", "connectivity_check")
                .build();
            
            PeriodicWorkRequest connectivityRequest = new PeriodicWorkRequest.Builder(
                BackgroundWorker.class, 30, TimeUnit.MINUTES)
                .setConstraints(constraints)
                .setInputData(inputData)
                .addTag(CONNECTIVITY_WORK)
                .build();
            
            WorkManager.getInstance(context)
                .enqueueUniquePeriodicWork(CONNECTIVITY_WORK,
                    androidx.work.ExistingPeriodicWorkPolicy.REPLACE,
                    connectivityRequest);
            
            Log.d(TAG, "Connectivity check scheduled");
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to schedule connectivity check", e);
        }
    }
    
    /**
     * Schedule data synchronization work
     */
    public static void scheduleDataSync(Context context) {
        try {
            Constraints constraints = new Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build();
            
            Data inputData = new Data.Builder()
                .putString("work_type", "data_sync")
                .build();
            
            PeriodicWorkRequest dataSyncRequest = new PeriodicWorkRequest.Builder(
                BackgroundWorker.class, 1, TimeUnit.HOURS)
                .setConstraints(constraints)
                .setInputData(inputData)
                .addTag(DATA_SYNC_WORK)
                .build();
            
            WorkManager.getInstance(context)
                .enqueueUniquePeriodicWork(DATA_SYNC_WORK,
                    androidx.work.ExistingPeriodicWorkPolicy.REPLACE,
                    dataSyncRequest);
            
            Log.d(TAG, "Data sync scheduled");
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to schedule data sync", e);
        }
    }
    
    /**
     * Schedule immediate one-time work
     */
    public static void scheduleImmediateWork(Context context, String workType) {
        try {
            Data inputData = new Data.Builder()
                .putString("work_type", workType)
                .build();
            
            OneTimeWorkRequest immediateRequest = new OneTimeWorkRequest.Builder(BackgroundWorker.class)
                .setInputData(inputData)
                .build();
            
            WorkManager.getInstance(context).enqueue(immediateRequest);
            
            Log.d(TAG, "Immediate work scheduled: " + workType);
            
        } catch (Exception e) {
            Log.e(TAG, "Failed to schedule immediate work", e);
        }
    }
    
    /**
     * Cancel all scheduled work
     */
    public static void cancelAllWork(Context context) {
        try {
            WorkManager.getInstance(context).cancelAllWork();
            Log.d(TAG, "All scheduled work cancelled");
        } catch (Exception e) {
            Log.e(TAG, "Failed to cancel work", e);
        }
    }
    
    /**
     * Initialize all background work scheduling
     */
    public static void initializeAllWork(Context context) {
        schedulePeriodicHealthCheck(context);
        scheduleConnectivityCheck(context);
        scheduleDataSync(context);
        Log.d(TAG, "All background work initialized");
    }
}