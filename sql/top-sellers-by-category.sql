WITH sales_data AS (
    SELECT
        o.seller_id,
        o.quantity,
        p.price,
        p.category_id,
        c.name AS category_name
    FROM orders o
    JOIN pets p ON o.pet_id = p.id
    JOIN categories c ON p.category_id = c.id
    WHERE o.placed_at >= CURRENT_DATE - INTERVAL '2 months'
      AND o.status IN ('approved', 'delivered')
),
category_totals AS (
    SELECT
        category_id,
        category_name,
        SUM(quantity) AS total_qty
    FROM sales_data
    GROUP BY category_id, category_name
),
top_category AS (
    SELECT category_id, category_name
    FROM category_totals
    ORDER BY total_qty DESC
    LIMIT 1
),
seller_totals AS (
    SELECT
        s.seller_id,
        u.username AS seller_name,
        SUM(s.quantity) AS qty_sold,
        SUM(s.quantity * s.price) AS total_price
    FROM sales_data s
    JOIN users u ON s.seller_id = u.id
    WHERE s.category_id = (SELECT category_id FROM top_category)
    GROUP BY s.seller_id, u.username
)
SELECT
    tc.category_name AS category,
    st.seller_name,
    st.qty_sold,
    st.total_price
FROM top_category tc
CROSS JOIN (
    SELECT seller_name, qty_sold, total_price
    FROM seller_totals
    ORDER BY qty_sold DESC
    LIMIT 10
) st
ORDER BY st.qty_sold DESC;