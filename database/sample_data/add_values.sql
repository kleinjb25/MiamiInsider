-- Adds some sample values to the database
-- IMPORTANT: If you want to add images as well, you need to use the /post_loc route
INSERT INTO categories VALUES (1, 'Restaurants', 'utensils');
INSERT INTO categories VALUES (2, 'Clinics', 'suitcase-medical');
INSERT INTO categories VALUES (3, 'Bars', 'beer-mug-empty');
INSERT INTO categories VALUES (4, 'Hotels', 'hotel');

INSERT INTO locations VALUES (1, -- ID
    'Fiesta Charra',    -- Name
    '25 W High St, Oxford, OH 45056',   -- Address
    'Roomy, booth-lined Mexican restaurant with a low-key vibe, a full bar & lunch specials.',  -- Description
    'N/A',  -- Email
    '(513) 524-3114',   -- Phone
    0,  -- Number of reviews
    NULL, -- Average rating
    1); -- Category

INSERT INTO locations VALUES (2, 'Brick Street Bar', '36 E High St, Oxford, OH 45056', 
    'Hopping hangout for live music, karaoke & TV sports with bar grub, drink specials & a patio.', 
    'brickstreet513@gmail.com', '(513) 280-6341', 0, NULL, 3);

