import sqlite3 from 'sqlite3'
import { open, Database } from 'sqlite'

import { DEBUGGER } from "./utilities";


type DB_HELPER = {
    id: number;
    use_count: number;
    is_closed: boolean;
    close: () => Promise<void>
}
type DB = Database<sqlite3.Database, sqlite3.Statement> & DB_HELPER


const DATABASE_COUNT = 10;

let _DB: Map<number, DB> = new Map<number, DB>();
// you would have to import / invoke this in another file

async function open_all_database() {
    for(const [id, db]of _DB.entries()) {
        await db.close();
    }

    _DB.clear()

    for(let i=0; i<DATABASE_COUNT; i++) {
        const db = await open({
            filename: "./roleplay.db",
            driver: sqlite3.Database
        }) as DB;

        function __dbclose(__db: Database<sqlite3.Database, sqlite3.Statement>) {
            return async () => {
                await __db.close();
            }    
        }

        db.id = i;
        db.use_count = 0;
        db.close = async () => {
            db.is_closed = true;
            await __dbclose(db)()
        }

        _DB.set(i, db);
    }
}

async function get_driver() {
    if(Array.from(_DB.entries()).length < DATABASE_COUNT) {
        await open_all_database();
    }

    let lowest_id = 0;
    let lowest_use_count = _DB.get(0)?.use_count ?? 1000000000;
    for(let i=0; i<DATABASE_COUNT; i++) {
        const db = _DB.get(i);
        if(!db) continue;
        if(db.use_count < lowest_use_count) {
            lowest_id = i;
            lowest_use_count = db.use_count;
        }
    }

    const retval = _DB.get(lowest_id);
    if(!retval) throw new Error("Internal Server Error: cannot create db");
    DEBUGGER.debug("Database", "Using driver id:", lowest_id)
    return retval
}


export default get_driver