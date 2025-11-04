CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(64) NOT NULL,
    notes VARCHAR(255) NULL,
    INDEX idx_expense_date (expense_date),
    INDEX idx_category_date (category, expense_date)
);
