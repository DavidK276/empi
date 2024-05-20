// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type { User } from '$lib/objects/user';
import type { Participant } from '$lib/objects/participant';
import type { Session } from 'svelte-kit-cookie-session';
import 'unplugin-icons/types/svelte';

declare global {
    namespace App {
        // interface Error {}
        interface Locals {
            user?: User,
            participant?: Participant,
            session: Session<SessionData>;
        }
        // interface PageData {
        //     session: SessionData;
        // }
        // interface PageState {}
        // interface Platform {}
    }
}

export {};
