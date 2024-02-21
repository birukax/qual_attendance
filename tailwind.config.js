/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./qual/qual/templates/**/*.html',
    './node_modules/flowbite/**/*.js',],
  theme: {
    extend: {
      colors: {
        primary: {"50":"#eff6ff","100":"#dbeafe","200":"#bfdbfe","300":"#93c5fd","400":"#60a5fa","500":"#3b82f6","600":"#2563eb","700":"#1d4ed8","800":"#1e40af","900":"#1e3a8a","950":"#172554"},
        'isabelline': { DEFAULT: '#edede9', 100: '#34342a', 200: '#676754', 300: '#989881', 400: '#c2c2b5', 500: '#edede9', 600: '#f0f0ed', 700: '#f4f4f2', 800: '#f8f8f6', 900: '#fbfbfb' }, 
        'timberwolf': { DEFAULT: '#d6ccc2', 100: '#312921', 200: '#625241', 300: '#937a62', 400: '#b6a391', 500: '#d6ccc2', 600: '#ded6ce', 700: '#e7e0da', 800: '#efebe7', 900: '#f7f5f3' }, 
        'linen': { DEFAULT: '#f5ebe0', 100: '#473017', 200: '#8e5f2e', 300: '#c78f52', 400: '#debd99', 500: '#f5ebe0', 600: '#f7efe6', 700: '#f9f3ed', 800: '#fbf7f3', 900: '#fdfbf9' }, 
        'champagne_pink': { DEFAULT: '#e3d5ca', 100: '#38291e', 200: '#70523b', 300: '#a87b59', 400: '#c5a891', 500: '#e3d5ca', 600: '#e8ddd4', 700: '#eee6df', 800: '#f4eeea', 900: '#f9f7f4' }, 
        'pale_dogwood': { DEFAULT: '#d5bdaf', 100: '#33241b', 200: '#664735', 300: '#986b50', 400: '#ba937c', 500: '#d5bdaf', 600: '#ddcabf', 700: '#e6d7cf', 800: '#eee4df', 900: '#f7f2ef' }
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

