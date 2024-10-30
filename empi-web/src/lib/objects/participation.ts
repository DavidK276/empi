import type { Research } from '$lib/objects/research';
import type { Participant } from '$lib/objects/participant';

export interface IParticipation {
	id: number;
	appointment: number;
	research: Research;
	participant: Participant;
	is_confirmed: boolean;
	token: string;
}