'use strict';
document.documentElement.classList.add('js');
const menuButton=document.querySelector('.navbar5_menu-button'),menu=document.querySelector('#mainMenu');
function closeMenu(){menu?.classList.remove('is-open');menuButton?.setAttribute('aria-expanded','false');menuButton?.setAttribute('aria-label','메뉴 열기');}
menuButton?.addEventListener('click',()=>{const open=menu.classList.toggle('is-open');menuButton.setAttribute('aria-expanded',String(open));menuButton.setAttribute('aria-label',open?'메뉴 닫기':'메뉴 열기');});
menu?.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menuButton?.getAttribute('aria-expanded')==='true'){closeMenu();menuButton.focus();}});
const dialog=document.getElementById('assistantDialog'),opener=document.getElementById('assistantOpen');
opener?.addEventListener('click',()=>dialog.showModal());
document.getElementById('assistantClose')?.addEventListener('click',()=>dialog.close());
dialog?.addEventListener('close',()=>opener.focus());
const year=document.getElementById('year');if(year)year.textContent=String(new Date().getFullYear());
// Preserve filenames; disclose unavailable media instead of showing false store imagery.
for(const img of document.querySelectorAll('img')){
 const failed=()=>{if(img.dataset.failed)return;img.dataset.failed='true';const note=document.createElement('p');note.className='missing-asset';note.textContent='이미지 준비 중: '+img.alt;img.hidden=true;img.after(note);};
 img.addEventListener('error',failed);if(img.complete&&img.naturalWidth===0)failed();
}
// Native video controls remain usable; motion is opt-in.
