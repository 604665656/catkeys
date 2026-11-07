#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 网页钢琴入门.html 改造成「喵琴师 · CatKeys」：改名 + 成就系统 + 体力/转发系统。
产出 catkeys/index.html（GitHub 单文件版）。dist 外置化在 build_dist.py。"""
import io, os, re, sys

SRC = r"C:/Users/60466/WorkBuddy/2026-11-07-09-39-46/piano_extract/网页钢琴入门.html"
OUT = r"C:/Users/60466/WorkBuddy/2026-11-07-09-39-46/catkeys/index.html"

with io.open(SRC, "r", encoding="utf-8") as f:
    t = f.read()

# ---------- 1. 改名 ----------
t = t.replace("<title>网页钢琴入门 · 节奏跟弹</title>",
              "<title>喵琴师 · CatKeys · 哈士喵的钢琴</title>")
t = t.replace("  网页钢琴入门 · 单文件可运行原型（零构建、零依赖）",
              "  喵琴师 · CatKeys · 单文件可运行原型（零构建、零依赖）")
t = t.replace(
    '  <div class="brand">🎹 网页钢琴入门<small>FALLING NOTES · RHYTHM TRAINER</small></div>',
    '  <div class="brand">🐱 喵琴师<small>CATKEYS · 哈士喵的钢琴</small></div>')
# 小猫吉祥物定名「哈士喵」
t = t.replace("小猫", "哈士喵")

# ---------- 2. 注入 CSS ----------
CSS = r"""
/* ══ 喵琴师 · 成就 / 体力 / 转发 ══ */
.chip.ach{color:var(--gold);border-color:var(--gold)}
.chip.ach b{color:var(--gold)}
.badge.stm{display:flex;align-items:center;gap:5px;padding:3px 6px}
.badge.stm .stmIco{color:var(--gold);font-size:12px}
.badge.stm b{color:var(--gold);font-variant-numeric:tabular-nums}
.stmBar{display:inline-block;width:46px;height:7px;border-radius:99px;background:rgba(255,255,255,.12);overflow:hidden;vertical-align:middle}
.stmBar i{display:block;height:100%;width:100%;background:linear-gradient(90deg,var(--gold),var(--acc));transition:width .3s}
.shareBtn{margin-left:2px;padding:4px 8px;border-radius:99px;border:1px solid var(--acc);
  background:linear-gradient(120deg,var(--acc),var(--acc2));color:var(--bg);font-size:10px;font-weight:800;cursor:pointer;white-space:nowrap}
.shareBtn:disabled{filter:grayscale(.6);cursor:not-allowed;opacity:.5}
.achList{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
.achItem{display:flex;gap:9px;align-items:center;padding:9px 10px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid transparent}
.achItem.locked{opacity:.5}
.achItem .achIco{font-size:24px;line-height:1;filter:grayscale(.2)}
.achBody{flex:1;min-width:0}
.achName{font-size:12px;font-weight:800;color:var(--txt)}
.achDesc{font-size:10px;color:var(--dim);line-height:1.35;margin-top:1px}
.achGot{font-size:10px;color:var(--gold);font-weight:800;white-space:nowrap}
.top{flex-wrap:wrap}
.chips{flex-wrap:wrap;justify-content:flex-end}
@media (max-width:560px){ .achList{grid-template-columns:1fr} .badge.stm .stmBar{display:none} }
"""
t = t.replace("</style>", CSS + "\n</style>", 1)

# ---------- 3. 注入顶栏：成就芯片 + 体力徽标 ----------
OLD_BADGE = '    <div class="badge" id="layoutBadge" title="点击选择键位密度 / 设备布局">键位 <b>—</b> ⌄</div>'
NEW_BADGE = OLD_BADGE + """
    <div class="chip ach" id="achChip" title="查看成就（喵琴师的挑战）">🏆 成就 <b id="achCount">0/10</b></div>
    <div class="badge stm" id="stmBadge" title="体力：每 60 秒恢复 1 点；分享可得体力">
      <span class="stmIco">⚡</span><b id="stmNum">5</b>/5
      <span class="stmBar"><i id="stmFill"></i></span>
      <button id="shareBtn" class="shareBtn" type="button">📤 分享得体力</button>
    </div>"""
t = t.replace(OLD_BADGE, NEW_BADGE, 1)

# ---------- 4. 注入成就弹窗 ----------
OLD_AUDIO = '<audio id="bgAudio" style="display:none"></audio>'
ACH_MODAL = r"""
<div class="modal" id="achModal"><div class="card">
  <h2>🏆 成就</h2>
  <div class="sub">完成挑战解锁成就 · 进度自动保存在本机</div>
  <div id="achList" class="achList"></div>
  <div class="btns"><button id="closeAch" class="primary">继续练习</button></div>
</div></div>
""" + OLD_AUDIO
t = t.replace(OLD_AUDIO, ACH_MODAL, 1)

# ---------- 5. startRun 体力门禁 ----------
OLD_START = "async function startRun(type){\n  await resumeAudio(); stopRun(); S.preview=false; demoIdx=0;"
NEW_START = (
    "async function startRun(type){\n"
    "  if(type==='game'||type==='cat'){\n"
    "    if(!canStartGame()){ promptNoStamina(); return; }\n"
    "    consumeStamina();\n"
    "  }\n"
    "  await resumeAudio(); stopRun(); S.preview=false; demoIdx=0;")
t = t.replace(OLD_START, NEW_START, 1)

# ---------- 6. finish() 结算时评定成就 ----------
OLD_FINISH = "  $('#resultModal').classList.add('show');"
NEW_FINISH = (
    "  const _newAch=evaluateAchievements({mode:'game',acc:acc,maxCombo:S.maxCombo,miss:S.miss,total:tot,speed:S.speed});\n"
    "  if(_newAch.length){ const _names=_newAch.map(a=>a.icon+a.name).join(' '); const _r=$('#rUnlock'); if(_r) _r.innerHTML=(_r.innerHTML||'')+'<br>🏆 新成就：'+_names; }\n"
    + OLD_FINISH)
t = t.replace(OLD_FINISH, NEW_FINISH, 1)

# ---------- 7. catFinish() 评小猫成就 ----------
OLD_CATFIN = "$('#catOver').classList.add('show');\n  updateCatHUD(); updateFab();"
NEW_CATFIN = (
    "$('#catOver').classList.add('show');\n"
    "  evaluateAchievements({mode:'cat',cleared:clear,maxCombo:CAT.maxCombo});\n"
    "  updateCatHUD(); updateFab();")
t = t.replace(OLD_CATFIN, NEW_CATFIN, 1)

# ---------- 8. updateFab 体力不足提示 ----------
OLD_FAB = "    b.classList.toggle('attention',S.mode==='game'||S.mode==='cat'||dead); b.classList.remove('busy');"
NEW_FAB = (OLD_FAB + "\n"
    "    if(!S.running && (S.mode==='game'||S.mode==='cat') && stamina.energy<=0){\n"
    "      b.innerHTML='⚡ 体力不足<small>点「📤 分享得体力」回体力</small>';\n"
    "    }")
t = t.replace(OLD_FAB, NEW_FAB, 1)

# ---------- 9. 注入 JS 主模块 ----------
JS = r"""
/* ════════════════ 喵琴师 · 成就 / 体力 / 转发 系统 ════════════════ */
progress.ach = progress.ach || {};
const ACHIEVEMENTS = [
  {id:'first',      icon:'🐾', name:'初遇',       desc:'完成你的第一首跟弹曲目'},
  {id:'full_combo', icon:'🔗', name:'全连',       desc:'单局零 MISS（≥20 音符）'},
  {id:'perfect',    icon:'💎', name:'完美主义',   desc:'单局准确率 100%（全 PERFECT）'},
  {id:'centurion',  icon:'🔥', name:'百连',       desc:'单局最大连击 ≥ 100'},
  {id:'triple',     icon:'⭐', name:'三星演奏家', desc:'任意曲目拿到 ★★★'},
  {id:'maestro',    icon:'🎼', name:'钢琴大师',   desc:'累计 ★ 达到 30'},
  {id:'graduate',   icon:'🏛️', name:'演奏级',     desc:'解锁 Lv.10 演奏级'},
  {id:'cat_clear',  icon:'🐱', name:'哈士喵通关', desc:'跳跃模式整首零踩空 CLEAR'},
  {id:'cat_king',   icon:'👑', name:'跳跃王者',   desc:'跳跃最远连跳 ≥ 50'},
  {id:'speed',      icon:'⚡', name:'极速指法',   desc:'≥120% 速度下完成一首（准确率≥55%）'}
];
function updateAchChip(){
  const n=(progress.ach&&Object.keys(progress.ach).length)||0;
  const el=$('#achCount'); if(el) el.textContent=n+'/'+ACHIEVEMENTS.length;
}
function renderAchModal(){
  const box=$('#achList'); if(!box) return; box.innerHTML='';
  ACHIEVEMENTS.forEach(a=>{
    const got=!!(progress.ach&&progress.ach[a.id]);
    const d=document.createElement('div');
    d.className='achItem'+(got?'':' locked');
    d.innerHTML='<div class="achIco">'+(got?a.icon:'🔒')+'</div>'+
      '<div class="achBody"><div class="achName">'+a.name+'</div>'+
      '<div class="achDesc">'+(got?a.desc:'未解锁 · '+a.desc)+'</div></div>'+
      (got?'<div class="achGot">已达成</div>':'');
    box.appendChild(d);
  });
}
function syncAchievements(){
  const met={};
  if(Object.keys(progress.best||{}).length>=1) met.first=true;
  if(Object.values(progress.stars||{}).some(v=>v>=3)) met.triple=true;
  if(totalStars()>=30) met.maestro=true;
  if(unlockedLevel()>=MAX_LV) met.graduate=true;
  let changed=false;
  ACHIEVEMENTS.forEach(a=>{ if(met[a.id]&&!progress.ach[a.id]){ progress.ach[a.id]=Date.now(); changed=true; } });
  if(changed) saveProgress();
  updateAchChip();
}
function evaluateAchievements(ctx){
  const met={};
  if(Object.keys(progress.best||{}).length>=1) met.first=true;
  if(Object.values(progress.stars||{}).some(v=>v>=3)) met.triple=true;
  if(totalStars()>=30) met.maestro=true;
  if(unlockedLevel()>=MAX_LV) met.graduate=true;
  if(ctx&&ctx.mode==='game'){
    if(ctx.miss===0&&ctx.total>=20) met.full_combo=true;
    if(ctx.acc>=0.999&&ctx.total>=10) met.perfect=true;
    if(ctx.maxCombo>=100) met.centurion=true;
    if(ctx.speed>=1.2&&ctx.acc>=0.55&&ctx.total>=10) met.speed=true;
  }
  if(ctx&&ctx.mode==='cat'){
    if(ctx.cleared) met.cat_clear=true;
    if(ctx.maxCombo>=50) met.cat_king=true;
  }
  const newly=[];
  ACHIEVEMENTS.forEach(a=>{ if(met[a.id]&&!progress.ach[a.id]){ progress.ach[a.id]=Date.now(); newly.push(a); } });
  if(newly.length){ saveProgress(); updateAchChip(); const names=newly.map(a=>a.icon+a.name).join(' '); toast('🏆 解锁成就：'+names); }
  return newly;
}

/* —— 体力 + 转发 —— */
const STM_KEY='catkeys_stamina_v1';
const STM_MAX=5, STM_RECOVER_MS=60000, STM_DAILY_CAP=20, STM_SHARE_MAX=3, STM_SHARE_GAP=15000, STM_SHARE_STAY=5000;
let stamina={energy:STM_MAX, lastTs:Date.now(), dailyPlay:0, dailyDate:'', shares:[], lastShareTs:0, sharePending:0, shareStart:0};
function sameDay(ts){ const d=new Date(ts), n=new Date(); return d.getFullYear()===n.getFullYear()&&d.getMonth()===n.getMonth()&&d.getDate()===n.getDate(); }
function saveStamina(){ try{ localStorage.setItem(STM_KEY,JSON.stringify(stamina)); }catch(e){} }
function loadStamina(){
  try{ const raw=localStorage.getItem(STM_KEY); if(raw){ const s=JSON.parse(raw); if(s&&typeof s==='object') stamina=Object.assign(stamina,s); } }catch(e){}
  const d=new Date(), key=d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
  if(stamina.dailyDate!==key){ stamina.dailyDate=key; stamina.dailyPlay=0; }
  stamina.shares=(stamina.shares||[]).filter(sameDay);
  recoverStamina(true); saveStamina();
}
function recoverStamina(silent){
  const now=Date.now();
  if(stamina.energy<STM_MAX){
    const rec=Math.floor((now-stamina.lastTs)/STM_RECOVER_MS);
    if(rec>0){ stamina.energy=Math.min(STM_MAX,stamina.energy+rec); stamina.lastTs+=rec*STM_RECOVER_MS; if(!silent) saveStamina(); }
  } else stamina.lastTs=now;
}
function renderStamina(){
  recoverStamina(true);
  const n=$('#stmNum'), f=$('#stmFill'), b=$('#shareBtn');
  if(n) n.textContent=stamina.energy;
  if(f) f.style.width=(stamina.energy/STM_MAX*100)+'%';
  if(b){
    const full=stamina.shares.length>=STM_SHARE_MAX, gap=Date.now()-stamina.lastShareTs<STM_SHARE_GAP;
    b.disabled=full||gap; b.style.opacity=(full||gap)?0.45:1;
    b.title=full?'今日分享已达上限（3 次）':gap?'分享太频繁，稍后再试':'分享链接并回到本页停留 5 秒得体力';
  }
}
function canStartGame(){ recoverStamina(true); return stamina.energy>0 && stamina.dailyPlay<STM_DAILY_CAP; }
function consumeStamina(){
  recoverStamina(true);
  if(!canStartGame()) return false;
  stamina.energy--; stamina.dailyPlay++; stamina.lastTs=Date.now();
  saveStamina(); renderStamina(); return true;
}
function promptNoStamina(){
  recoverStamina(true);
  if(stamina.dailyPlay>=STM_DAILY_CAP){ toast('今日游玩已达上限（'+STM_DAILY_CAP+' 局），明天再来吧～'); return; }
  toast('⚡ 体力不足！点右上角「📤 分享得体力」回体力');
}
function doShare(){
  recoverStamina(true);
  if(stamina.shares.length>=STM_SHARE_MAX){ toast('今日分享已达上限（3 次）'); return; }
  if(Date.now()-stamina.lastShareTs<STM_SHARE_GAP){ toast('分享太频繁，15 秒后再试'); return; }
  const base=location.href.split('#')[0];
  const link=base+(base.indexOf('?')>=0?'&':'?')+'from=catkeys';
  try{ if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(link); }catch(e){}
  stamina.sharePending=1; stamina.shareStart=Date.now(); stamina.lastShareTs=Date.now();
  saveStamina(); renderStamina();
  toast('🔗 分享链接已复制！去分享给好友，回到本页停留 5 秒即可领取体力 ⚡');
}
function onReturn(){
  recoverStamina(true);
  if(!stamina.sharePending) return;
  if(Date.now()-stamina.shareStart<STM_SHARE_STAY) return;
  stamina.sharePending=0;
  if(stamina.shares.length>=STM_SHARE_MAX){ saveStamina(); renderStamina(); return; }
  stamina.shares.push(Date.now()); stamina.energy=Math.min(STM_MAX,stamina.energy+1);
  saveStamina(); renderStamina();
  toast('🎉 分享成功，体力 +1（'+stamina.energy+'/'+STM_MAX+'）');
}
/* 初始化 */
loadStamina(); renderStamina(); syncAchievements();
setInterval(()=>{ recoverStamina(false); renderStamina(); updateAchChip(); }, 10000);
document.addEventListener('visibilitychange',()=>{ if(!document.hidden) onReturn(); });
window.addEventListener('focus',onReturn);
$('#achChip').addEventListener('click',()=>{ renderAchModal(); $('#achModal').classList.add('show'); });
$('#closeAch').addEventListener('click',()=>$('#achModal').classList.remove('show'));
$('#achModal').addEventListener('click',e=>{ if(e.target.id==='achModal') $('#achModal').classList.remove('show'); });
$('#shareBtn').addEventListener('click',doShare);
"""
t = t.replace("boot();\n</script>", JS + "\nboot();\n</script>", 1)

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(t)

# 自检：关键替换是否生效
checks = {
    "喵琴师标题": "喵琴师 · CatKeys" in t,
    "哈士喵吉祥物": "哈士喵" in t,
    "成就芯片": 'id="achChip"' in t,
    "体力徽标": 'id="stmBadge"' in t,
    "分享按钮": 'id="shareBtn"' in t,
    "成就弹窗": 'id="achModal"' in t,
    "startRun门禁": "canStartGame()" in t,
    "finish评定": "evaluateAchievements({mode:'game'" in t,
    "catFinish评定": "evaluateAchievements({mode:'cat'" in t,
    "updateFab体力": "体力不足" in t,
    "JS模块": "const ACHIEVEMENTS" in t,
}
print("== 替换自检 ==")
for k,v in checks.items():
    print(("OK  " if v else "FAIL")+k)
print("index.html 字节数:", len(t.encode("utf-8")))
if not all(checks.values()):
    print("存在失败项，退出"); sys.exit(1)
print("DONE")
