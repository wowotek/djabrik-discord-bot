import get_driver from "./driver";
import { DEBUGGER } from "./utilities";

type Constructor<T> = { new (...args: Array<any>): T }
class Model {
    static model_name: string;
    private _id: number;

    constructor(id: number) { this._id = id }
    public get id() { return this._id; }

    static getColumnNameTypes(): string { throw new Error("cannot call this from super.context") }

    static async checkTableExistance() {
        const driver = await get_driver();
        try {
            DEBUGGER.log("Database", "┌ Checking Database Existance:", this.model_name)
            const mdl = await driver.get('SELECT * FROM ' + this.model_name);
            if(mdl && mdl.length > 0) {
                if(Object.getOwnPropertyNames(mdl[0]).length != Object.getOwnPropertyNames(this).length) {
                    DEBUGGER.error("Database", "├ Column count does not match. please manualy migrate");
                }
            }
            DEBUGGER.log("Database", "└ Done !");
        } catch(e) {
            DEBUGGER.error("Database", e)
            try {
                DEBUGGER.error("Database", "├ Database not found, creating one");
                await driver.exec('CREATE TABLE ' + this.model_name + this.getColumnNameTypes())
                DEBUGGER.log("Database", "└ Done !");
            } catch {
                DEBUGGER.error("Database", "└ Fatal Error, cannot create database. exiting...");
                process.exit(1);
            }
        }
    }

    protected static async __getOneById<T={ [keys: string]: any }>(id: number): Promise<T> {
        const driver = await get_driver();
        return await driver.get(`SELECT * FROM ${this.model_name} WHERE id = ?`, id) as T;
    }

    protected static async __getAll<T={ [keys: string]: any }>(): Promise<Array<T>> {
        const driver = await get_driver();
        return await driver.get(`SELECT * FROM ${this.model_name}`) as Array<T>;
    }
    
    protected static async __createOne<T={ [keys: string]: any }>(obj: { [keys: string]: any}): Promise<T | null> {
        const keys = Object.getOwnPropertyNames(obj);
        const question_mark = [];
        const values = [];
        for(const key of keys) {
            values.push(obj[key])
            question_mark.push("?")
        }

        const driver = await get_driver();
        const result = await driver.run(`INSERT INTO ${this.model_name} (${keys.join(",")}) VALUES (${question_mark.join(",")})`, ...values)
        if (result.lastID) {
            return await this.__getOneById(result.lastID)
        }
        return null;
    }

    protected static async __updateOne<T={ [keys: string]: any }>(id: string, obj: { [keys: string]: any }): Promise<T | null> {
        if('id' in obj) try {
            delete obj["id"];
        } catch {
            try { delete obj.id } catch {}
        }

        const keys = Object.getOwnPropertyNames(obj);
        const values = [];
        for(const key of keys) {
            values.push(`${key}=?`)
        }

        const driver = await get_driver()
        const result = await driver.run(`UPDATE ${this.model_name} SET ${values.join(",")} WHERE id=?`, ...values, id)
        if (result.lastID) {
            return await this.__getOneById(result.lastID)
        }
        return null;
    }
}

export class Player extends Model {
    static model_name = "player";

    private _regist_date: Date;
    private _regist_answer_reason: string;
    private _regist_answer_expectation: string;
    private constructor(
        discord_id: number,
        regist_date: Date,
        regist_answer_reason: string,
        regist_answer_expectation: string
    ) {
        super(discord_id);
        this._regist_date = regist_date;
        this._regist_answer_reason = regist_answer_reason;
        this._regist_answer_expectation = regist_answer_expectation;
    }

    get regist_date() { return this._regist_date; }
    get regist_answer_reason() { return this._regist_answer_reason; }
    get regist_answer_expectation() { return this._regist_answer_expectation; }

    static getColumnNameTypes(): string {
        return " (\
            id INTEGER,\
            regist_date REAL,\
            regist_answer_reason TEXT,\
            regist_answer_expectation TEXT\
        )"
    }

    public static async getOneById(id: number) {
        const p = await this.__getOneById(id);
        return new Player(p.id, p.regist_date, p.regist_answer_reason, p.regist_answer_expectation);
    }

    public static async getAll() {
        const ps = await this.__getAll();
        const po = []
        for(const p of ps) {
            po.push(new Player(p.id, p.regist_date, p.regist_answer_reason, p.regist_answer_expectation));
        }

        return po
    }

    public static async createOne(
        discord_id: number,
        regist_date: Date,
        regist_answer_reason: string,
        regist_answer_expectation: string
    ){
        const p = await this.__createOne({
            id: discord_id,
            regist_date,
            regist_answer_reason,
            regist_answer_expectation,
        })

        if(!p) return p;
        return new Player(p.id, p.regist_date, p.regist_answer_reason, p.regist_answer_expectation);
    }
}

export class PlayerAttendance extends Model {
    
}

export class PlayerPointAccount extends Model {
    static model_name = "player_point_account";
    private _is_deposit: boolean;
    private _date: Date;
    private _amount: number;
    private _reason: string;

    private constructor(
        id: number,
        is_deposit: boolean,
        date: Date,
        amount: number,
        reason: string = "",
    ) {
        super(id);
        this._is_deposit = is_deposit;
        this._date = date;
        this._amount = amount;
        this._reason = reason;
    }
    get is_deposit() { return this._is_deposit; }
    get date() { return this._date; }
    get amount() { return this._amount; }
    get reason() { return this._reason; }

    static getColumnNameTypes(): string {
        return " (\
            id INTEGER,\
            is_deposit BOOLEAN,\
            date REAL,\
            amount INTEGER\
        )"
    }
}

(async () => {
    await Player.checkTableExistance()
})()