import { globalStyle, style } from '@vanilla-extract/css';
import { vars } from './theme.css';

export const row = style({
	display: 'flex',
	flexDirection: 'row',
	gap: vars.md,
	selectors: {
		'.ver-top&': {
			alignItems: 'top'
		},
		'.ver-center&': {
			alignItems: 'center'
		},
		'.hor-left&': {
			justifyContent: 'start'
		},
		'.hor-center&': {
			justifyContent: 'center'
		}
	},
	'@media': {
		'screen and (max-width: 768px)': {
			selectors: {
				'.m-col&': {
					flexDirection: 'column'
				}
			}
		}
	}
});

export const col = style({
	display: 'flex',
	flexDirection: 'column',
	gap: vars.md,
	selectors: {
		'.ver-top&': {
			alignItems: 'top'
		},
		'.ver-center&': {
			alignItems: 'center'
		},
		'.hor-left&': {
			justifyContent: 'start'
		},
		'.hor-center&': {
			justifyContent: 'center'
		}
	}
});

export const dropdown = style({
	display: 'inline-block',
	'@media': {
		'screen and (min-width: 768px)': {
			position: 'relative',
			float: 'left'
		}
	}
});

export const dropdownContent = style({
	display: 'none',
	position: 'absolute',
	right: 0,
	left: 0,
	margin: '0 auto',
	width: 'fit-content',
	boxShadow: '0px 8px 16px 0px rgba(0,0,0,0.4)',
	backgroundColor: vars.backgroundPrimary,
	zIndex: 1,
	borderRadius: vars.sm,
	paddingLeft: vars.lg,
	paddingRight: vars.lg,
	paddingTop: vars.lg,
	paddingBottom: vars.lg,
	gap: vars.lg,
	selectors: {
		[`${dropdown}:hover &,${dropdown}.show &`]: {
			display: 'flex'
		}
	}
});

export const content = style({
	maxWidth: 1280,
	width: '100%'
});

export const hidden = style({
	display: 'none'
});

export const error = style({
	color: 'red',
	display: 'block',
	margin: '4px 0'
});

export const box = style({
	border: '1px solid gray',
	borderRadius: vars.xs,
	boxShadow: '0 0 4px gray',
	margin: `${vars.sm} 0`,
	padding: `${vars.sm}`
});

export const accordion = style({
	border: `1px solid ${vars.buttonPrimary}`,
	borderRadius: vars.xs,
	overflow: 'hidden',
});

export const accordionTabContent = style({
	maxHeight: 0,
	overflow: 'hidden',
});

export const accordionTab = style({});

export const accordionTabLabel = style({
	cursor: 'pointer',
	padding: vars.sm,
	backgroundColor: vars.buttonPrimary,
	color: vars.textSecondary,
	justifyContent: 'space-between'
});

export const accordionTabInput = style({
	position: 'absolute',
	opacity: 0,
	zIndex: -1
});

globalStyle(`${accordionTab} input:checked ~ ${accordionTabContent}`, {
	maxHeight: 'initial',
	margin: vars.sm
});