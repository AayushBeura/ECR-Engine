-- Enable pg_cron extension if not already enabled (requires superuser)
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule a nightly job at 3:00 AM to delete old transaction logs
-- Purpose limitation: Delete SMS/UPI logs older than 6 months
SELECT cron.schedule(
    'purge_old_transaction_logs',   -- Job Name
    '0 3 * * *',                    -- Cron schedule (Every day at 3:00 AM)
    $$ 
    DELETE FROM transaction_logs 
    WHERE created_at < NOW() - INTERVAL '6 months'; 
    $$                              -- Command to execute
);
