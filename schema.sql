CREATE TABLE plans (
  id                     SERIAL PRIMARY KEY,
  name                   VARCHAR(50) NOT NULL UNIQUE,
  max_tracked_categories INT NOT NULL,
  price                  NUMERIC(10, 2) NOT NULL,
  created_at             TIMESTAMP DEFAULT NOW()
);

INSERT INTO plans (name, max_tracked_categories, price) VALUES
  ('free',    4,  0.00),
  ('pro',     10, 4.99),
  ('premium', 25, 9.99);

CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  email      VARCHAR(255) NOT NULL UNIQUE,
  plan_id    INT REFERENCES plans(id) ON DELETE SET NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE categories (
  id    SERIAL PRIMARY KEY,
  label VARCHAR(100) NOT NULL,
  value VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE deals (
  id             SERIAL PRIMARY KEY,
  name           VARCHAR(255) NOT NULL,
  category_id    INT REFERENCES categories(id) ON DELETE SET NULL,
  original_price NUMERIC(10, 2) NOT NULL,
  current_price  NUMERIC(10, 2) NOT NULL,
  img_url        TEXT,
  src_url        TEXT NOT NULL,
  created_at     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_tracked_categories (
  id          SERIAL PRIMARY KEY,
  user_id     INT REFERENCES users(id) ON DELETE CASCADE,
  category_id INT REFERENCES categories(id) ON DELETE CASCADE,
  UNIQUE(user_id, category_id)
);

CREATE TABLE user_deal_history (
  id        SERIAL PRIMARY KEY,
  user_id   INT REFERENCES users(id) ON DELETE CASCADE,
  deal_id   INT REFERENCES deals(id) ON DELETE CASCADE,
  viewed_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, deal_id)
);

-- Notification channels available
CREATE TABLE notification_channels (
  id      SERIAL PRIMARY KEY,
  name    VARCHAR(50) NOT NULL UNIQUE  -- 'email', 'whatsapp', 'sms'
);

INSERT INTO notification_channels (name) VALUES
  ('email'),
  ('whatsapp'),
  ('sms');

-- User notification preferences
CREATE TABLE user_notifications (
  id          SERIAL PRIMARY KEY,
  user_id     INT REFERENCES users(id) ON DELETE CASCADE,
  channel_id  INT REFERENCES notification_channels(id) ON DELETE CASCADE,
  destination VARCHAR(255) NOT NULL,  -- email address or phone number
  is_active   BOOLEAN DEFAULT TRUE,
  created_at  TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, channel_id)  -- one preference per channel per user
);