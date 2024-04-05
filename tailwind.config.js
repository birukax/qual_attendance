/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./qual/qual/templates/**/*.html',
    './node_modules/flowbite/**/*.js',],
  theme: {
    extend: {
      colors: {
        primary: { "50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd", "400": "#60a5fa", "500": "#3b82f6", "600": "#2563eb", "700": "#1d4ed8", "800": "#1e40af", "900": "#1e3a8a", "950": "#172554" },
        'isabelline': { DEFAULT: '#edede9', 100: '#34342a', 200: '#676754', 300: '#989881', 400: '#c2c2b5', 500: '#edede9', 600: '#f0f0ed', 700: '#f4f4f2', 800: '#f8f8f6', 900: '#fbfbfb' },
        'timberwolf': { DEFAULT: '#d6ccc2', 100: '#312921', 200: '#625241', 300: '#937a62', 400: '#b6a391', 500: '#d6ccc2', 600: '#ded6ce', 700: '#e7e0da', 800: '#efebe7', 900: '#f7f5f3' },
        'linen': { DEFAULT: '#f5ebe0', 100: '#473017', 200: '#8e5f2e', 300: '#c78f52', 400: '#debd99', 500: '#f5ebe0', 600: '#f7efe6', 700: '#f9f3ed', 800: '#fbf7f3', 900: '#fdfbf9' },
        'champagne_pink': { DEFAULT: '#e3d5ca', 100: '#38291e', 200: '#70523b', 300: '#a87b59', 400: '#c5a891', 500: '#e3d5ca', 600: '#e8ddd4', 700: '#eee6df', 800: '#f4eeea', 900: '#f9f7f4' },
        'pale_dogwood': { DEFAULT: '#d5bdaf', 100: '#33241b', 200: '#664735', 300: '#986b50', 400: '#ba937c', 500: '#d5bdaf', 600: '#ddcabf', 700: '#e6d7cf', 800: '#eee4df', 900: '#f7f2ef' },
        'seasalt': { DEFAULT: '#f8f9fa', 100: '#29323a', 200: '#536475', 300: '#8496a8', 400: '#bfc8d1', 500: '#f8f9fa', 600: '#fafbfc', 700: '#fbfcfc', 800: '#fdfdfd', 900: '#fefefe' },
        'anti-flash_white': { DEFAULT: '#e9ecef', 100: '#282f37', 200: '#505f6e', 300: '#7c8ea0', 400: '#b3bec8', 500: '#e9ecef', 600: '#eef1f3', 700: '#f3f4f6', 800: '#f7f8f9', 900: '#fbfbfc' },
        'platinum': { DEFAULT: '#dee2e6', 100: '#272d34', 200: '#4e5b67', 300: '#788899', 400: '#abb6c0', 500: '#dee2e6', 600: '#e5e9ec', 700: '#eceef1', 800: '#f2f4f5', 900: '#f9f9fa' },
        'french_gray': { DEFAULT: '#ced4da', 100: '#242a30', 200: '#495561', 300: '#6d7f91', 400: '#9da9b5', 500: '#ced4da', 600: '#d7dce1', 700: '#e1e5e9', 800: '#ebeef0', 900: '#f5f6f8' },
        'french_gray': { DEFAULT: '#adb5bd', 100: '#202428', 200: '#404850', 300: '#616d79', 400: '#85919d', 500: '#adb5bd', 600: '#bdc4ca', 700: '#ced3d8', 800: '#dee1e5', 900: '#eff0f2' },
        'slate_gray': { DEFAULT: '#6c757d', 100: '#161819', 200: '#2c2f32', 300: '#41474b', 400: '#575e64', 500: '#6c757d', 600: '#899199', 700: '#a7adb2', 800: '#c4c8cc', 900: '#e2e4e5' },
        'outer_space': { DEFAULT: '#495057', 100: '#0e1011', 200: '#1d2022', 300: '#2b2f34', 400: '#3a3f45', 500: '#495057', 600: '#68727d', 700: '#8c959f', 800: '#b2b9bf', 900: '#d9dcdf' },
        'onyx': { DEFAULT: '#343a40', 100: '#0b0c0d', 200: '#15171a', 300: '#202327', 400: '#2a2f34', 500: '#343a40', 600: '#58626c', 700: '#7d8995', 800: '#a9b0b8', 900: '#d4d8dc' },
        'eerie_black': { DEFAULT: '#212529', 100: '#070808', 200: '#0e0f11', 300: '#141719', 400: '#1b1f22', 500: '#212529', 600: '#49525b', 700: '#6f7d8b', 800: '#9fa8b2', 900: '#cfd4d8' }

      }
    },
  },
  fontFamily: {
    'body': [
      'Inter',
      'ui-sans-serif',
      'system-ui',
      '-apple-system',
      'system-ui',
      'Segoe UI',
      'Roboto',
      'Helvetica Neue',
      'Arial',
      'Noto Sans',
      'sans-serif',
      'Apple Color Emoji',
      'Segoe UI Emoji',
      'Segoe UI Symbol',
      'Noto Color Emoji'
    ],
    'sans': [
      'Inter',
      'ui-sans-serif',
      'system-ui',
      '-apple-system',
      'system-ui',
      'Segoe UI',
      'Roboto',
      'Helvetica Neue',
      'Arial',
      'Noto Sans',
      'sans-serif',
      'Apple Color Emoji',
      'Segoe UI Emoji',
      'Segoe UI Symbol',
      'Noto Color Emoji'
    ]
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

