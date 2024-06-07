
DROP TRIGGER IF EXISTS auto_delete;
# 创建触发器，删除账户时自动减少用户的账户数

CREATE Trigger auto_delete
AFTER DELETE ON mybanksystem_customer_account FOR EACH ROW
BEGIN
    UPDATE mybanksystem_bank_customer SET accounts_cnt = accounts_cnt - 1 WHERE id = OLD.user_id;
END;
