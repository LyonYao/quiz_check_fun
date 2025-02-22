
CREATE EXTENSION pg_cron;


CREATE OR REPLACE FUNCTION delete_stale_records()
RETURNS void AS $$
DECLARE
    r RECORD;
BEGIN
    -- 开始事务
    BEGIN;
    WITH deleted_a AS (
        DELETE FROM quiz.activity_reg  WHERE reg_time < now() - interval '3 months' RETURNING reg_code;
    )
    
     WITH deleted_b AS (
        DELETE FROM quiz.check_record WHERE reg_code IN (SELECT reg_code FROM deleted_a) RETURNING id;
    )
    DELETE FROM quiz.check_answer WHERE record_id IN (SELECT id FROM deleted_b);
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- 如果出现任何错误，回滚事务
        ROLLBACK;
        RAISE;
END;
$$ LANGUAGE plpgsql;

SELECT cron.schedule('0 0 1 * *', 'SELECT delete_stale_records();');
