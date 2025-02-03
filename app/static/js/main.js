import { ClassicEditor, AccessibilityHelp, Autosave, Bold, Essentials, Italic, Paragraph, SelectAll, Undo } from 'ckeditor5';

const editorConfig = {
	toolbar: {
		items: ['undo', 'redo', '|', 'selectAll', '|', 'bold', 'italic', '|', 'accessibilityHelp'],
		shouldNotGroupWhenFull: false
	},
	plugins: [AccessibilityHelp, Autosave, Bold, Essentials, Italic, Paragraph, SelectAll, Undo],		
	placeholder: 'Type or paste your content here!',
    width:'100%'
};

ClassicEditor.create(document.querySelector('#editor'), editorConfig);
