<script lang="ts">
    import markdownit from 'markdown-it';
    import type { PageProps } from './$types';
    import UserPasswordRequiredModal from '$lib/components/UserPasswordRequiredModal.svelte';
    import { t } from '$lib/translations';
    import { page } from '$app/state';
    import { enhance } from '$app/forms';
    import MaterialSymbolsInfoOutline from 'virtual:icons/material-symbols/info-outline';
    import { localeDateStringFromUTCString } from '$lib/functions';
    import { universalEnhance } from "$lib/enhanceFunctions";

    let { data }: PageProps = $props();

    const converter = markdownit();
</script>
{#if page.data.user != null}
    <UserPasswordRequiredModal></UserPasswordRequiredModal>
{/if}
<div class="row m-col heading">
    <h1>{data.research?.name}</h1>
    {#await data.participations then participations}
	    {@const participationConfirmed = participations?.values().some(p => p.is_confirmed)}
        {#if participationConfirmed}
            <div class="row ver-center no-gap">
                <MaterialSymbolsInfoOutline width="24"
                                            height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.participated')}
            </div>
        {/if}
    {/await}
</div>
<div class="col no-gap">
    {#if data.research?.comment}
        <hr>
    {/if}
    <!-- eslint-disable-next-line svelte/no-at-html-tags -- Rendering using markdownit is safe. -->
    {@html converter.render(data.research?.comment ?? "")}
    {#if data.research?.comment}
        <hr>
    {/if}
</div>
{#if data.research?.info_url}
	<span>{$t('research.info_url_introduction')} <a href={data.research?.info_url}
                                                    target="_blank">{$t('research.here')}</a></span>
{/if}
{#await data.participations}
    <p>{$t('common.loading')}</p>
{:then participations}
    {#each data.appointments as appointment, i (appointment.id)}
        {@const participation = participations?.get(appointment.id)}
        {@const participationConfirmed = participation?.is_confirmed === true}
        {@const signupsLapsed = new Date(appointment.when) < new Date()}
        {@const canSignup = participation == null && !signupsLapsed && appointment.free_capacity > 0}
        <div class="box">
            <div class="row ver-center">
                <h2>{$t('research.appointment_number')} {i + 1}</h2>
                {#if appointment.location}
                    <button>{$t('research.in_person')}</button>
                {:else}
                    <button>{$t('research.online')}</button>
                {/if}
                {#if participation != null}
                    <button style="background: var(--success)">
                        {#if participationConfirmed}
                            {$t('research.participation_confirmed')}
                        {:else}
                            {$t('research.appointment_signedup')}
                        {/if}
                    </button>
                {/if}
                {#if signupsLapsed}
				<span class="row ver-center no-gap">
					<MaterialSymbolsInfoOutline width="24"
                                                height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.signups_lapsed')}</span>
                {/if}
            </div>
            <p>{appointment.comment}</p>
            <div style="width: 50%" class="m-w-full">
                <table style="width: 100%; margin-bottom: var(--sm)">
                    <thead>
                    <tr>
                        <th>{$t('research.when')}</th>
                        {#if appointment.location}
                            <th>{$t('research.location')}</th>
                        {:else if participation != null && !participationConfirmed}
                            <th>{$t('research.join_appointment_url')}</th>
                        {/if}
                        <th>{$t('research.free_capacity')}</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>
                            <time datetime="{appointment.when}">{localeDateStringFromUTCString(appointment.when)}</time>
                        </td>
                        {#if appointment.location}
                            <td>{appointment.location}</td>
                        {:else if participation != null && !participationConfirmed}
                            <td><a href={appointment.info_url} target="_blank">{$t('research.join_appointment')}</a>
                            </td>
                        {/if}
                        <td style="text-align: center">
						<span
                            style="color: {appointment.free_capacity ? 'var(--text-primary)' : 'red'}">{appointment.free_capacity}</span>
                        </td>
                    </tr>
                    </tbody>
                </table>
                {#if canSignup}
                    <form method="POST" action="?/signup" use:enhance={({formElement, submitter}) => {
					return universalEnhance({formElement, submitter}, {
						idleMessage: $t('common.login'),
						runningMessage: $t('common.logging_in'),
						reset: false,
						invalidateAll: true
					});
				}}>
                        <input type="hidden" name="appointment" value={appointment.id}>
                        {#if page.data.user == null}
                            <label for="recipient">Email</label>
                            <input type="email" name="recipient" id="recipient" class="m-w-full">
                        {/if}
                        <div class="row ver-center" id="submit-div">
                            <button type="submit">{$t('research.signup')}</button>
                            {#if page.data.user == null}
							<span class="row ver-center no-gap">
								<MaterialSymbolsInfoOutline width="24" height="24"
                                ></MaterialSymbolsInfoOutline>&nbsp;{$t('research.anonymous_signup')}
							</span>
                            {/if}
                        </div>
                    </form>
                {/if}
                {#if participation != null && !participationConfirmed}
                    <form method="POST" action="?/cancel" use:enhance={({formElement, submitter}) => {
					return universalEnhance({formElement, submitter}, {
						idleMessage: $t('common.logout'),
						runningMessage: $t('common.logging_out'),
						reset: false,
						invalidateAll: true
					});
				}}>
                        <input type="hidden" name="participation-id" value={participation?.id}>
                        <button type="submit" style="background: var(--danger)">{$t('research.cancel')}</button>
                    </form>
                {/if}
            </div>
        </div>
    {:else}
        <div class="row ver-center no-gap">
            <MaterialSymbolsInfoOutline width="24"
                                        height="24"></MaterialSymbolsInfoOutline>&nbsp;{$t('research.no_appointments')}
        </div>
    {/each}
{/await}
