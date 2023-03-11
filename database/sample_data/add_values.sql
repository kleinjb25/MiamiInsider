-- Adds some sample values to the database

-- This user's password is 'password123'
INSERT INTO users VALUES (1, 'Test', 'User', 'test@miamioh.edu', 'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e', 0, NULL, 1);

INSERT INTO categories VALUES (1, 'Restaurants', 'utensils');
INSERT INTO categories VALUES (2, 'Clinics', 'suitcase-medical');
INSERT INTO categories VALUES (3, 'Bars', 'beer-mug-empty');
INSERT INTO categories VALUES (4, 'Hotels', 'hotel');


-- IMPORTANT: If you want to add images as well, you need to use the /post_loc route
INSERT INTO locations VALUES (1, -- ID
    'Fiesta Charra',    -- Name
    '25 W High St, Oxford, OH 45056',   -- Address
    'Roomy, booth-lined Mexican restaurant with a low-key vibe, a full bar & lunch specials.',  -- Description
    'N/A',  -- Email
    '(513) 524-3114',   -- Phone
    3,  -- Number of reviews
    3.6, -- Average rating
    1); -- Category

INSERT INTO locations VALUES (2, 'Brick Street Bar', '36 E High St, Oxford, OH 45056', 
    'Hopping hangout for live music, karaoke & TV sports with bar grub, drink specials & a patio.', 
    'brickstreet513@gmail.com', '(513) 280-6341', 2, 4, 3);

-- Reviews for Fiesta Charra
INSERT INTO reviews VALUES (1, 1, 1, 4, 'Pretty good, I got wasted and vomited all over my friend');
INSERT INTO reviews VALUES (2, 1, 1, 2, 'Their service is subpar');
INSERT INTO reviews VALUES (3, 1, 1, 5, 'Best Mexican food I have ever eaten');

-- Reviews for Fiesta Charra
INSERT INTO reviews VALUES (4, 1, 2, 3, 'It''s a decent place, I don''t really get what all the excitement is about though.');
INSERT INTO reviews VALUES (5, 1, 2, 5, 'Hungover as fuck rn');