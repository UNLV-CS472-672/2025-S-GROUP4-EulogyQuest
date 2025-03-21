DELIMITER $$

DROP PROCEDURE IF EXISTS insert_npc;

CREATE PROCEDURE insert_npc()
BEGIN
    -- Declare variables
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
    SET zone_id = 189;
    SET zone_name = 'tutorialb';  -- example zone

    SET x_pos = -44;
    SET y_pos = -103; 
    SET z_pos = 21;
    SET heading = 363;

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
        INSERT INTO npc_types SET id=npc_id, name="TestBot_0", lastname="", level="1", race="457", class="1", bodytype="5", hp="10000000", mana="0", gender="2", texture="0", helmtexture="0", herosforgemodel="0", size="10", hp_regen_rate="1000", hp_regen_per_second="0", mana_regen_rate="0", loottable_id="0", merchant_id="0", greed="0", alt_currency_id="0", npc_spells_id="0", npc_spells_effects_id="0", npc_faction_id="0", adventure_template_id="0", trap_template="0", mindmg="1", maxdmg="5000", attack_count="-1", npcspecialattks="", special_abilities="", aggroradius="70", assistradius="0", face="0", luclin_hairstyle="0", luclin_haircolor="0", luclin_eyecolor="0", luclin_eyecolor2="0", luclin_beardcolor="0", luclin_beard="0", drakkin_heritage="0", drakkin_tattoo="0", drakkin_details="0", armortint_id="0", armortint_red="0", armortint_green="0", armortint_blue="0", d_melee_texture1="0", d_melee_texture2="0", ammo_idfile="IT10", prim_melee_type="28", sec_melee_type="28", ranged_type="7", runspeed="1.25", MR="1000", CR="1000", DR="1000", FR="1000", PR="1000", Corrup="1000", PhR="1000", see_invis="0", see_invis_undead="0", qglobal="0", AC="12", npc_aggro="0", spawn_limit="0", attack_speed="0", attack_delay="30", findable="0", STR="12", STA="12", DEX="12", AGI="12", _INT="12", WIS="12", CHA="12", see_hide="0", see_improved_hide="0", trackable="1", isbot="0", exclude="1", ATK="0", Accuracy="0", Avoidance="0", slow_mitigation="0", version="0", maxlevel="0", scalerate="100", private_corpse="0", unique_spawn_by_name="0", underwater="0", isquest="1", emoteid="0", spellscale="100", healscale="100", no_target_hotkey="0", raid_target="0", armtexture="0", bracertexture="0", handtexture="0", legtexture="0", feettexture="0", light="0", walkspeed="0", peqid="0", unique_="0", fixed="0", ignore_despawn="0", show_name="1", untargetable="0", charm_ac="0", charm_min_dmg="0", charm_max_dmg="0", charm_attack_delay="0", charm_accuracy_rating="0", charm_avoidance_rating="0", charm_atk="0", skip_global_loot="0", rare_spawn="0", stuck_behavior="0", model="0", flymode="-1", always_aggro="0", exp_mod="100", heroic_strikethrough="0", faction_amount="0", keeps_sold_items="1", is_parcel_merchant="0", multiquest_enabled="0";

        SET spawngroup_id = (SELECT max(id)+1 AS id FROM spawngroup);
        SET spawngroup_name = CONCAT(zone_name, '_', spawngroup_id);

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

        
        -- Insert into spawn2 --19 rows insert
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
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No available NPC ID in this zone.';
    END IF;
END $$

DELIMITER ;

CALL insert_npc();
