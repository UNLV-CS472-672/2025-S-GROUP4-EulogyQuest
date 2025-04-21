START TRANSACTION;

-- npc_type_insert
INSERT INTO npc_types (id, name, lastname, level, texture, helmtexture, face, race, gender, isquest) VALUES (2000100, 'Hollidays', 'ghost', 60, 1, 1, 2, 1, 0, 1) ON DUPLICATE KEY UPDATE name=VALUES(name), lastname=VALUES(lastname), level=VALUES(level), isquest=VALUES(isquest);
INSERT INTO npc_types (id, name, lastname, level, texture, helmtexture, face, race, gender, isquest) VALUES (2000101, 'Ada', 'Larkin', 60, 2, 0, 4, 1, 0, 1) ON DUPLICATE KEY UPDATE name=VALUES(name), lastname=VALUES(lastname), level=VALUES(level), isquest=VALUES(isquest);
INSERT INTO npc_types (id, name, lastname, level, texture, helmtexture, face, race, gender, isquest) VALUES (2000102, 'Mister', 'Dunne', 60, 1, 0, 6, 1, 0, 1) ON DUPLICATE KEY UPDATE name=VALUES(name), lastname=VALUES(lastname), level=VALUES(level), isquest=VALUES(isquest);
INSERT INTO npc_types (id, name, lastname, level, texture, helmtexture, face, race, gender, isquest) VALUES (2000103, 'Pastor', 'Crowley', 60, 3, 0, 5, 1, 0, 1) ON DUPLICATE KEY UPDATE name=VALUES(name), lastname=VALUES(lastname), level=VALUES(level), isquest=VALUES(isquest);
INSERT INTO npc_types (id, name, lastname, level, texture, helmtexture, face, race, gender, isquest) VALUES (2000104, 'Sylas', 'Wren', 60, 2, 1, 3, 1, 0, 1) ON DUPLICATE KEY UPDATE name=VALUES(name), lastname=VALUES(lastname), level=VALUES(level), isquest=VALUES(isquest);

-- spawngroup_insert
INSERT INTO spawngroup (id, name, spawn_limit, delay, mindelay, despawn, dist, max_x, min_x, max_y, min_y) VALUES (2000100, 'tutorialb_2000100', 1, 120000, 120000, 0, 0, 0, 0, 0, 0) ON DUPLICATE KEY UPDATE spawn_limit=VALUES(spawn_limit);
INSERT INTO spawngroup (id, name, spawn_limit, delay, mindelay, despawn, dist, max_x, min_x, max_y, min_y) VALUES (2000101, 'tutorialb_2000101', 1, 120000, 120000, 0, 0, 0, 0, 0, 0) ON DUPLICATE KEY UPDATE spawn_limit=VALUES(spawn_limit);
INSERT INTO spawngroup (id, name, spawn_limit, delay, mindelay, despawn, dist, max_x, min_x, max_y, min_y) VALUES (2000102, 'tutorialb_2000102', 1, 120000, 120000, 0, 0, 0, 0, 0, 0) ON DUPLICATE KEY UPDATE spawn_limit=VALUES(spawn_limit);
INSERT INTO spawngroup (id, name, spawn_limit, delay, mindelay, despawn, dist, max_x, min_x, max_y, min_y) VALUES (2000103, 'tutorialb_2000103', 1, 120000, 120000, 0, 0, 0, 0, 0, 0) ON DUPLICATE KEY UPDATE spawn_limit=VALUES(spawn_limit);
INSERT INTO spawngroup (id, name, spawn_limit, delay, mindelay, despawn, dist, max_x, min_x, max_y, min_y) VALUES (2000104, 'tutorialb_2000104', 1, 120000, 120000, 0, 0, 0, 0, 0, 0) ON DUPLICATE KEY UPDATE spawn_limit=VALUES(spawn_limit);

-- spawnentry_insert
INSERT INTO spawnentry (spawngroupID, npcID, chance) VALUES (2000100, 2000100, 100) ON DUPLICATE KEY UPDATE chance=VALUES(chance);
INSERT INTO spawnentry (spawngroupID, npcID, chance) VALUES (2000101, 2000101, 100) ON DUPLICATE KEY UPDATE chance=VALUES(chance);
INSERT INTO spawnentry (spawngroupID, npcID, chance) VALUES (2000102, 2000102, 100) ON DUPLICATE KEY UPDATE chance=VALUES(chance);
INSERT INTO spawnentry (spawngroupID, npcID, chance) VALUES (2000103, 2000103, 100) ON DUPLICATE KEY UPDATE chance=VALUES(chance);
INSERT INTO spawnentry (spawngroupID, npcID, chance) VALUES (2000104, 2000104, 100) ON DUPLICATE KEY UPDATE chance=VALUES(chance);

-- spawn2_insert
INSERT INTO spawn2 (id, spawngroupID, zone, x, y, z, heading) VALUES (3266100, 2000100, 'tutorialb', -72.26, -192.6, 15.09, 0.0) ON DUPLICATE KEY UPDATE x=VALUES(x), y=VALUES(y), z=VALUES(z), heading=VALUES(heading);
INSERT INTO spawn2 (id, spawngroupID, zone, x, y, z, heading) VALUES (3266101, 2000101, 'tutorialb', -62.77, -193.64, 16.17, 0.0) ON DUPLICATE KEY UPDATE x=VALUES(x), y=VALUES(y), z=VALUES(z), heading=VALUES(heading);
INSERT INTO spawn2 (id, spawngroupID, zone, x, y, z, heading) VALUES (3266102, 2000102, 'tutorialb', -51.89, -183.39, 14.4, 0.0) ON DUPLICATE KEY UPDATE x=VALUES(x), y=VALUES(y), z=VALUES(z), heading=VALUES(heading);
INSERT INTO spawn2 (id, spawngroupID, zone, x, y, z, heading) VALUES (3266103, 2000103, 'tutorialb', -41.97, -178.06, 13.36, 0.0) ON DUPLICATE KEY UPDATE x=VALUES(x), y=VALUES(y), z=VALUES(z), heading=VALUES(heading);
INSERT INTO spawn2 (id, spawngroupID, zone, x, y, z, heading) VALUES (3266104, 2000104, 'tutorialb', -72.72, -195.64, 34.2, 0.0) ON DUPLICATE KEY UPDATE x=VALUES(x), y=VALUES(y), z=VALUES(z), heading=VALUES(heading);

COMMIT;