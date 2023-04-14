-- Adds some sample values to the database

-- The user passwords are 'password123'
INSERT INTO users VALUES (0, -- ID
'Admin',  -- First name
'User',   -- Last name
'admin@miamioh.edu',  -- Email
'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e',   -- Password (hashed)
NULL, -- Phone number
1,    -- Private (0=false, 1=true)
99);  -- Permission (0=none, 99=admin)
INSERT INTO users VALUES (1, 'John', 'Doe', 'doejh14@miamioh.edu', 'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e', '(513) 433-4884', 1, 0);
INSERT INTO users VALUES (2, 'Mary', 'Smith', 'smithma@miamioh.edu', 'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e', '(812) 498-1193', 0, 0);
INSERT INTO users VALUES (3, 'Jim', 'Buckington', 'buckinjr@miamioh.edu', 'pbkdf2:sha256:260000$wmVhehZVBBrDErgB$0705ae78c87fb6ac8487724fdcfe5193cec39ce6c3f930455c435d052277329e', NULL, 1, 0);

INSERT INTO categories VALUES (1, -- ID 
'Restaurants', -- Name
'utensils');   -- fa-tag (for icons from fontawesome)
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
INSERT INTO locations VALUES (3, 'McCullough-Hyde Memorial Hospital', '110 N Poplar St, Oxford, OH 45056', 
    'McCullough-Hyde Memorial Hospital is proud of our almost 60 year history and comprehensive service to Oxford, Ohio, and the surrounding area. We are a comprehensive, fully accredited hospital with highly trained staff and state-of-the-art equipment. McCullough Hyde serves almost 100,000 people annually. This includes more than 2,000 admissions, over 15,000 emergency room visits, more than 80,000 outpatient visits, and more than 400 new babies each year.', 
    'patientrelations@trihealth.com', '(513) 569-6111', 0, NULL, 2);

-- Reviews for Fiesta Charra
INSERT INTO reviews VALUES (1, -- ID 
1, -- User ID
'John Doe',   -- User name
1,  -- Location ID
'Fiesta Charra',  -- Location name
4,  -- Review (# of stars)
'Pretty good, I got wasted and vomited all over my friend'); -- Review text
INSERT INTO reviews VALUES (2, 2, 'Mary Smith', 1, 'Fiesta Charra', 2, 'Their service is subpar');
INSERT INTO reviews VALUES (3, 1, 'John Doe', 1, 'Fiesta Charra', 5, 'Best Mexican food I have ever eaten');

-- Reviews for Brick Street Bar
INSERT INTO reviews VALUES (4, 2, 'Mary Smith', 2, 'Brick Street Bar', 3, 'It''s a decent place, I don''t really get what all the excitement is about though.');
INSERT INTO reviews VALUES (5, 1, 'John Doe', 2, 'Brick Street Bar', 5, 'Hungover as fuck rn');