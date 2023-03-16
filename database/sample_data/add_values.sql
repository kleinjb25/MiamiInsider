-- Adds some sample values to the database

-- The user passwords are 'password123'
INSERT INTO users VALUES (1, 'John', 'Doe', 'doejh14@miamioh.edu', 'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e', '(513) 433-4884', 1);
INSERT INTO users VALUES (2, 'Mary', 'Smith', 'smithma@miamioh.edu', 'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e', '(812) 498-1193', 1);

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
INSERT INTO reviews VALUES (1, 1, 'John Doe', 1, 'Fiesta Charra', 4, 'Pretty good, I got wasted and vomited all over my friend');
INSERT INTO reviews VALUES (2, 2, 'Mary Smith', 1, 'Fiesta Charra', 2, 'Their service is subpar');
INSERT INTO reviews VALUES (3, 1, 'John Doe', 1, 'Fiesta Charra', 5, 'Best Mexican food I have ever eaten');

-- Reviews for Fiesta Charra
INSERT INTO reviews VALUES (4, 2, 'Mary Smith', 2, 'Brick Street Bar', 3, 'It''s a decent place, I don''t really get what all the excitement is about though.');
INSERT INTO reviews VALUES (5, 1, 'John Doe', 2, 'Brick Street Bar', 5, 'Hungover as fuck rn');