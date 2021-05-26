package ai.databand;

import ai.databand.log.HistogramRequest;
import org.apache.log4j.spi.LoggingEvent;
import org.apache.spark.scheduler.SparkListenerStageCompleted;
import org.apache.spark.sql.Dataset;

import java.lang.reflect.Method;
import java.util.Map;

/**
 * No-op run used when no tracking is available to avoid unnecessary exceptions and log pollution.
 */
public class NoopDbndRun implements DbndRun {

    @Override
    public void init(Method method, Object[] args) {
        // do nothing
    }

    @Override
    public void startTask(Method method, Object[] args) {
        // do nothing
    }

    @Override
    public void errorTask(Method method, Throwable error) {
        // do nothing
    }

    @Override
    public void completeTask(Method method, Object result) {
        // do nothing
    }

    @Override
    public void stop() {
        // do nothing
    }

    @Override
    public void error(Throwable error) {
        // do nothing
    }

    @Override
    public void logMetric(String key, Object value) {
        // do nothing
    }

    @Override
    public void logDataframe(String key, Dataset<?> value, HistogramRequest withHistograms) {
        // do nothing
    }

    @Override
    public void logHistogram(Map<String, Object> histogram) {
        // do nothing
    }

    @Override
    public void logMetrics(Map<String, Object> metrics) {
        // do nothing
    }

    @Override
    public void logMetrics(Map<String, Object> metrics, String source) {
        // do nothing
    }

    @Override
    public void saveLog(LoggingEvent event, String formattedEvent) {
        // do nothing
    }

    @Override
    public void saveSparkMetrics(SparkListenerStageCompleted event) {
        // do nothing
    }

    @Override
    public String getTaskName(Method method) {
        // dummy
        return method.getName();
    }
}