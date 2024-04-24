export class Appointment {
	id!: number;
	research!: number;
	when!: string;
	capacity!: number;
	free_capacity!: number;
	comment!: string;
	location!: string;
	info_url!: string;

	getUTCDatetimeAndOffset(): { datetime: string, offset: string } {
		const sign = this.when[19];
		const [datetime, offset] = this.when.split(sign);
		return {
			datetime,
			offset: sign + offset
		};
	}
}