DELIMITER $$

DROP PROCEDURE IF EXISTS insert_npc;

CREATE PROCEDURE insert_npc()
BEGIN
    -- Declare variables, following database structures
    DECLARE npc_id INT;
    DECLARE spawngroup_id INT;

    DECLARE zone_id INT;
    DECLARE zone_name VARCHAR(32);

    DECLARE x_pos FLOAT(14,6);
    DECLARE y_pos FLOAT(14,6);
    DECLARE z_pos FLOAT(14,6);
    DECLARE heading FLOAT(14,6);

    DECLARE spawngroup_name VARCHAR(200);

    -- Initialize variables
    SET zone_id = 189; -- Only used to get npc_id, database uses 6 digit npc_ids formatted as <zone_id> _ _ _ 
    SET zone_name = 'tutorialb';  -- the tutorial zone's shortname - IMPORTANT

    ------------------------------------
    -- CHANGE WHERE THE NPC SPAWNS HERE
    -- ---------------------------------
    SET x_pos = 0;   --x val   from #loc
    SET y_pos = 0;   --y val   from #loc
    SET z_pos = 0;   --z val   from #loc
    SET heading = 0; --heading from #loc

    -- Find the next available primary key (id number) for our NPC entry
    SET npc_id = (
        SELECT MIN(t1.id + 1)
        FROM npc_types t1
        LEFT JOIN npc_types t2 ON t1.id + 1 = t2.id
        WHERE t1.id LIKE CONCAT(zone_id, '%') AND t2.id IS NULL
    );

    -- If we found an available ID, insert the NPC, otherwise throw an error
    IF npc_id IS NOT NULL THEN
        -- Insert into npc_types

        ------------------------------------------------------------
        -- PASTE YOUR NPC SQL COMMAND HERE
        -- Dont forget to change UPDATE -> INSERT INTO and <id> -> npc_id

        -- Dont forget to delete the 'WHERE id = <id>' at the end -->
        -- END PASTE SECTION
        -------------------------------------------------------------

        -- This gets the next available ID (primary key) for the spawngroup table
        -- spawngroup_id is used to associate all 3 spawn tables
        SET spawngroup_id = (SELECT max(id)+1 AS id FROM spawngroup);

        -- PEQ uses this as the default name, good enough for me!
        SET spawngroup_name = CONCAT(zone_name, '_', spawngroup_id);

        -- Spawn entries below, the variables we care about (for now) are at the top
        -- Insert into spawngroup -- count = 13
        INSERT INTO spawngroup
            SET id=spawngroup_id, 
                name=spawngroup_name, 
                spawn_limit="0", 
                dist = "0", 
                max_x = "0", 
                min_x = "0", 
                max_y = "0", 
                min_y = "0", 
                delay = "45000", 
                mindelay = "15000", 
                despawn = "0", 
                despawn_timer = "100", 
                wp_spawns = "0"
            ;

        -- Insert into spawnentry -- count = 10
        INSERT INTO spawnentry 
            SET spawngroupID=spawngroup_id, 
                npcID=npc_id, 
                chance=100, 
                condition_value_filter=1, 
                min_time=0, 
                max_time=0, 
                min_expansion=-1, 
                max_expansion=-1, 
                content_flags=NULL, 
                content_flags_disabled=NULL
            ; 

        -- pathgrid is here, currently unsupported
        -- Insert into spawn2 -- count = 19
        INSERT INTO spawn2
            SET id=NULL, 
                spawngroupID=spawngroup_id, 
                zone=zone_name, 
                version=0, 
                x=x_pos, 
                y=y_pos, 
                z=z_pos, 
                heading=heading, 
                respawntime=1200, 
                variance=0, 
                pathgrid=0, 
                path_when_zone_idle=0, 
                _condition=0, 
                cond_value=1, 
                animation=0, 
                min_expansion=-1, 
                max_expansion=-1, 
                content_flags=NULL, 
                content_flags_disabled=NULL
            ;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No available NPC ID in zone';
    END IF;
END $$

DELIMITER ;

CALL insert_npc();
