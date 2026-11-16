const M=[['cintura','Cintura'],['quadril','Quadril'],['coxas','Coxas'],['panturrilhas','Panturrilhas'],['bracos','Braços'],['peitoral','Peitoral']];
const LBL=Object.fromEntries([['peso','Peso (kg)'],['altura','Altura (cm)'],...M.map(m=>[m[0],m[1]+' (cm)'])]);
let S={uid:null,view:'inicio',edit:null,metric:'peso',reg:false,a:'',b:''};
const $=s=>document.querySelector(s);
const esc=t=>String(t??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function ld(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){toast('Não foi possível salvar neste navegador.',1)}}
let DB=ld('bt_db',{users:[],recs:[]});
const save=()=>sv('bt_db',DB);
S.uid=null;
const me=()=>DB.users.find(u=>u.id===S.uid);
const mine=()=>DB.recs.filter(r=>r.uid===S.uid).sort((a,b)=>a.data<b.data?-1:1);
const today=()=>new Date(Date.now()-new Date().getTimezoneOffset()*6e4).toISOString().slice(0,10);
const fd=d=>d.split('-').reverse().join('/');
const nf=n=>n==null?'–':(+n).toLocaleString('pt-BR',{maximumFractionDigits:1});
const uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,7);
let tt;function toast(m,bad){const t=$('#toast');t.textContent=m;t.className='show'+(bad?' bad':'');clearTimeout(tt);tt=setTimeout(()=>t.className='',3200)}
async function hash(p,salt){const d=new TextEncoder().encode(salt+':'+p);
 const k=await crypto.subtle.importKey('raw',d,'PBKDF2',false,['deriveBits']);
 const b=await crypto.subtle.deriveBits({name:'PBKDF2',salt:new TextEncoder().encode(salt),iterations:100000,hash:'SHA-256'},k,256);
 return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')}
const num=v=>v===''||v==null?null:parseFloat(String(v).replace(',','.'));
const fe=(id,m)=>{const e=$('#e-'+id);if(e)e.textContent=m||''};

/* ---------- AUTH ---------- */
function authView(){
 const r=S.reg;
 $('#app').innerHTML=`<div class="auth card"><div class="brand">BodyTrack</div><h1>${r?'Criar conta':'Entrar'}</h1>
 <p class="muted">${r?'Cadastre-se para acompanhar seu peso e suas medidas.':'Acesse para ver sua evolução.'}</p>
 <div class="f" style="grid-template-columns:1fr">
 ${r?`<div><label for="nome">Nome</label><input id="nome" autocomplete="name"><p class="err" id="e-nome"></p></div>`:''}
 <div><label for="email">E-mail</label><input id="email" type="email" autocomplete="email"><p class="err" id="e-email"></p></div>
 <div><label for="senha">Senha</label><input id="senha" type="password" autocomplete="${r?'new-password':'current-password'}"><p class="err" id="e-senha"></p></div>
 ${r?`<div><label for="senha2">Confirmar senha</label><input id="senha2" type="password" autocomplete="new-password"><p class="err" id="e-senha2"></p></div>`:''}
 <button class="btn" id="go">${r?'Criar conta':'Entrar'}</button></div>
 <p class="muted" style="margin-bottom:0">${r?'Já tem conta?':'Ainda não tem conta?'} <button class="l" id="sw">${r?'Entrar':'Criar conta'}</button></p></div>`;
 $('#sw').onclick=()=>{S.reg=!S.reg;authView()};
 $('#go').onclick=r?doReg:doLogin;
 document.querySelectorAll('input').forEach(i=>i.onkeydown=e=>{if(e.key==='Enter')$('#go').click()});
}
function sync(u){const x=DB.users.find(y=>y.id===u.id);if(x){x.nome=u.nome;x.email=u.email}else DB.users.push({id:u.id,nome:u.nome,email:u.email,altura:null,nasc:''});save()}
async function doReg(){
 const nome=$('#nome').value.trim(),email=$('#email').value.trim().toLowerCase(),s=$('#senha').value,s2=$('#senha2').value;
 ['nome','email','senha','senha2'].forEach(i=>fe(i));
 let res,data;
 try{
  res=await fetch('/api/cadastro',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nome,email,senha:s,senha2:s2})});
  data=await res.json();
 }catch(e){toast('Não foi possível falar com o servidor.',1);return}
 if(!res.ok){fe(data.campo||'email',data.erro);return}
 sync(data.usuario);S.uid=data.usuario.id;S.view='inicio';
 toast(data.mensagem);render();
}
async function doLogin(){
 const email=$('#email').value.trim().toLowerCase(),s=$('#senha').value;fe('email');fe('senha');
 if(!email||!s){fe('senha','Informe e-mail e senha.');return}
 let res,data;
 try{
  res=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,senha:s})});
  data=await res.json();
 }catch(e){toast('Não foi possível falar com o servidor.',1);return}
 if(!res.ok){fe(data.campo||'senha',data.erro);return}
 sync(data.usuario);S.uid=data.usuario.id;S.view='inicio';
 toast(data.mensagem);render();
}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}S.uid=null;S.reg=false;toast('Você saiu da conta.');render()}

/* ---------- SHELL ---------- */
const NAV=[['inicio','Início'],['registrar','Registrar'],['historico','Histórico'],['evolucao','Evolução'],['perfil','Perfil']];
function render(){
 if(!me()){authView();return}
 $('#app').innerHTML=`<header class="top"><span class="brand">BodyTrack</span><button class="btn g" id="out">Sair</button></header><nav aria-label="Principal">
 ${NAV.map((n,i)=>`<button data-v="${n[0]}" class="${S.view===n[0]?'on':''}"><i aria-hidden="true">${'⌂+☰↗☺'[i]}</i>${n[1]}</button>`).join('')}</nav><main id="main"></main>`;
 document.querySelectorAll('nav [data-v]').forEach(b=>b.onclick=()=>{S.view=b.dataset.v;S.edit=null;render()});
 $('#out').onclick=logout;
 ({inicio:inicio,registrar:registrar,historico:historico,evolucao:evolucao,perfil:perfil})[S.view]();
}

/* ---------- CHART ---------- */
function chart(pts,unit){
 if(pts.length<2)return`<div class="empty">Registre ao menos dois valores para ver o gráfico.</div>`;
 const W=640,H=260,p={l:44,r:16,t:16,b:30};
 const ys=pts.map(q=>q.y);let mn=Math.min(...ys),mx=Math.max(...ys);if(mn===mx){mn-=1;mx+=1}
 const pad=(mx-mn)*.15;mn-=pad;mx+=pad;
 const t0=new Date(pts[0].x).getTime(),t1=new Date(pts[pts.length-1].x).getTime()||1;
 const X=x=>p.l+((new Date(x).getTime()-t0)/Math.max(t1-t0,1))*(W-p.l-p.r),Y=y=>p.t+(1-(y-mn)/(mx-mn))*(H-p.t-p.b);
 const line=pts.map((q,i)=>(i?'L':'M')+X(q.x).toFixed(1)+' '+Y(q.y).toFixed(1)).join(' ');
 const area=line+` L${X(pts[pts.length-1].x).toFixed(1)} ${H-p.b} L${X(pts[0].x).toFixed(1)} ${H-p.b} Z`;
 let g='';for(let i=0;i<4;i++){const v=mn+(mx-mn)*i/3,y=Y(v);g+=`<line x1="${p.l}" x2="${W-p.r}" y1="${y}" y2="${y}" stroke="#4d2539" stroke-width="1"/><text x="${p.l-6}" y="${y+4}" text-anchor="end" fill="#b88aa0" font-size="11">${nf(v)}</text>`}
 const dots=pts.map(q=>`<circle cx="${X(q.x).toFixed(1)}" cy="${Y(q.y).toFixed(1)}" r="4" fill="#ff7aa8" stroke="#1a0b14" stroke-width="2"><title>${fd(q.x)}: ${nf(q.y)} ${unit}</title></circle>`).join('');
 return`<svg class="ch" viewBox="0 0 ${W} ${H}" role="img" aria-label="Gráfico de evolução">
 <defs><linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0407f" stop-opacity=".45"/><stop offset="1" stop-color="#e0407f" stop-opacity="0"/></linearGradient></defs>
 ${g}<path d="${area}" fill="url(#gr)"/><path d="${line}" fill="none" stroke="#ff7aa8" stroke-width="2.5" stroke-linejoin="round"/>${dots}
 <text x="${p.l}" y="${H-8}" fill="#b88aa0" font-size="11">${fd(pts[0].x)}</text><text x="${W-p.r}" y="${H-8}" text-anchor="end" fill="#b88aa0" font-size="11">${fd(pts[pts.length-1].x)}</text></svg>`;
}
const series=(rs,k)=>rs.filter(r=>r[k]!=null).map(r=>({x:r.data,y:r[k]}));
const lastOf=(rs,k)=>{for(let i=rs.length-1;i>=0;i--)if(rs[i][k]!=null)return rs[i][k];return null};
const delta=(a,b,inv)=>{if(a==null||b==null)return'';const d=b-a;if(Math.abs(d)<.05)return'<small class="muted">sem variação</small>';return`<small class="${d>0?'up':'dn'}">${d>0?'+':''}${nf(d)} desde o início</small>`};

/* ---------- INÍCIO ---------- */
function inicio(){
 const rs=mine(),u=me(),sp=series(rs,'peso');
 const h=lastOf(rs,'altura')??u.altura,w=lastOf(rs,'peso');
 const imc=h&&w?w/Math.pow(h/100,2):null;
 const cls=imc==null?'':imc<18.5?'abaixo do peso':imc<25?'faixa normal':imc<30?'sobrepeso':'obesidade';
 $('#main').innerHTML=`<h2>Olá, ${esc(u.nome.split(' ')[0])}</h2>
 ${!rs.length?`<div class="card empty"><h3>Nenhum registro ainda</h3><p>Comece registrando seu peso e suas medidas de hoje.</p><button class="btn" id="n">Fazer primeiro registro</button></div>`:`
 <div class="grid" style="margin-bottom:16px">
 <div class="stat hero"><small>Peso atual</small><b>${nf(w)} kg</b>${delta(sp[0]?.y,w)}</div>
 <div class="stat"><small>Altura</small><b>${h?nf(h)+' cm':'–'}</b></div>
 <div class="stat"><small>IMC</small><b>${imc?nf(imc):'–'}</b><small>${cls}</small></div>
 <div class="stat"><small>Registros</small><b>${rs.length}</b><small>último em ${fd(rs[rs.length-1].data)}</small></div></div>
 <div class="card"><h3 style="margin-bottom:10px">Evolução do peso</h3>${chart(sp,'kg')}</div>
 <div class="card"><h3 style="margin-bottom:12px">Medidas mais recentes</h3><div class="grid">
 ${M.map(m=>{const s=series(rs,m[0]);return`<div class="stat"><small>${m[1]}</small><b>${nf(lastOf(rs,m[0]))}${s.length?' cm':''}</b>${delta(s[0]?.y,s[s.length-1]?.y)}</div>`}).join('')}</div></div>`}`;
 const n=$('#n');if(n)n.onclick=()=>{S.view='registrar';render()};
}

/* ---------- REGISTRAR / EDITAR ---------- */
function registrar(){
 const r=S.edit?DB.recs.find(x=>x.id===S.edit&&x.uid===S.uid):null;
 const v=k=>r&&r[k]!=null?r[k]:'';
 const h=r?r.altura:(lastOf(mine(),'altura')??me().altura);
 $('#main').innerHTML=`<h2>${r?'Editar registro':'Novo registro'}</h2><div class="card">
 <div class="f">
 <div><label for="data">Data</label><input id="data" type="date" max="${today()}" value="${r?r.data:today()}"><p class="err" id="e-data"></p></div>
 <div><label for="peso">Peso (kg)</label><input id="peso" inputmode="decimal" value="${v('peso')}" placeholder="ex.: 68,5"><p class="err" id="e-peso"></p></div>
 <div><label for="altura">Altura (cm)</label><input id="altura" inputmode="decimal" value="${h??''}" placeholder="ex.: 165"><p class="err" id="e-altura"></p></div></div>
 <h3 style="margin:18px 0 10px">Medidas corporais (cm)</h3><div class="f">
 ${M.map(m=>`<div><label for="${m[0]}">${m[1]}</label><input id="${m[0]}" inputmode="decimal" value="${v(m[0])}"><p class="err" id="e-${m[0]}"></p></div>`).join('')}
 <div class="full"><label for="obs">Observações (opcional)</label><textarea id="obs" rows="2" maxlength="300">${esc(r?.obs||'')}</textarea></div></div>
 <div class="row" style="margin-top:14px"><button class="btn" id="sv">${r?'Salvar alterações':'Salvar registro'}</button>${r?'<button class="btn g" id="cc">Cancelar</button>':''}</div></div>`;
 $('#sv').onclick=()=>saveRec(r);
 if(r)$('#cc').onclick=()=>{S.edit=null;S.view='historico';render()};
}
function saveRec(r){
 const rec={data:$('#data').value,obs:$('#obs').value.trim()};let ok=true,any=false;
 document.querySelectorAll('.err').forEach(e=>e.textContent='');
 if(!rec.data||rec.data>today()){fe('data','Escolha uma data que não seja futura.');ok=false}
 const rules={peso:[20,400],altura:[80,250],...Object.fromEntries(M.map(m=>[m[0],[10,250]]))};
 for(const k in rules){const raw=$('#'+k).value.trim(),n=num(raw);
  if(raw===''){rec[k]=null;continue}
  if(isNaN(n)||n<rules[k][0]||n>rules[k][1]){fe(k,`Informe um valor entre ${rules[k][0]} e ${rules[k][1]}.`);ok=false}else{rec[k]=n;if(k!=='altura')any=true}}
 if(ok&&!any){fe('peso','Preencha o peso ou ao menos uma medida.');ok=false}
 if(!ok){toast('Corrija os campos destacados.',1);return}
 if(r){Object.assign(r,rec);toast('Registro atualizado.')}
 else{DB.recs.push({id:uid(),uid:S.uid,...rec});toast('Registro salvo.')}
 if(rec.altura){const u=me();u.altura=rec.altura}
 save();S.edit=null;S.view='historico';render();
}

/* ---------- HISTÓRICO ---------- */
function historico(){
 const rs=mine().reverse();
 $('#main').innerHTML=`<h2>Histórico</h2>
 ${!rs.length?`<div class="card empty">Nenhum registro por aqui ainda.</div>`:`
 <div class="card"><div class="row" style="margin-bottom:12px"><div><label for="d1">De</label><input id="d1" type="date"></div><div><label for="d2">Até</label><input id="d2" type="date"></div></div>
 <div class="tbl"><table id="ht"><thead><tr><th>Data</th><th>Peso</th><th>Altura</th>${M.map(m=>`<th>${m[1]}</th>`).join('')}<th>Obs.</th><th></th></tr></thead><tbody id="tb"></tbody></table></div></div>`}`;
 if(!rs.length)return;
 const draw=()=>{const a=$('#d1').value,b=$('#d2').value;
  const f=rs.filter(r=>(!a||r.data>=a)&&(!b||r.data<=b));
  $('#tb').innerHTML=f.length?f.map(r=>`<tr><td class="dt" data-l=""><b>${fd(r.data)}</b></td><td data-l="Peso">${nf(r.peso)}</td><td data-l="Altura">${nf(r.altura)}</td>${M.map(m=>`<td data-l="${m[1]}">${nf(r[m[0]])}</td>`).join('')}<td class="o">${esc(r.obs)}</td>
  <td class="ac"><div class="row" style="flex-wrap:nowrap"><button class="btn g" data-e="${r.id}">Editar</button><button class="btn d" data-x="${r.id}">Excluir</button></div></td></tr>`).join(''):`<tr><td colspan="11" class="empty">Nenhum registro neste período.</td></tr>`;
  document.querySelectorAll('[data-e]').forEach(b=>b.onclick=()=>{S.edit=b.dataset.e;S.view='registrar';render()});
  document.querySelectorAll('[data-x]').forEach(b=>b.onclick=()=>{
   if(b.dataset.c){DB.recs=DB.recs.filter(r=>r.id!==b.dataset.x);save();toast('Registro excluído.');historico();return}
   b.dataset.c=1;b.textContent='Confirmar?';setTimeout(()=>{if(b.isConnected){delete b.dataset.c;b.textContent='Excluir'}},3500)});};
 $('#d1').onchange=$('#d2').onchange=draw;draw();
}

/* ---------- EVOLUÇÃO ---------- */
function evolucao(){
 const rs=mine(),k=S.metric,pts=series(rs,k);
 const ds=rs.map(r=>r.data);
 if(!S.a||!ds.includes(S.a))S.a=ds[0]||'';if(!S.b||!ds.includes(S.b))S.b=ds[ds.length-1]||'';
 $('#main').innerHTML=`<h2>Evolução</h2>${!rs.length?`<div class="card empty">Registre medidas para ver seus gráficos.</div>`:`
 <div class="card"><div class="pills">${Object.keys(LBL).map(x=>`<button class="pill ${x===k?'on':''}" data-m="${x}">${LBL[x].replace(/ \(.*/,'')}</button>`).join('')}</div>
 <h3 style="margin-bottom:8px">${LBL[k]}</h3>${chart(pts,k==='peso'?'kg':'cm')}</div>
 <div class="card"><h3 style="margin-bottom:12px">Comparar datas</h3><div class="row" style="margin-bottom:12px">
 <div><label for="ca">Data inicial</label><select id="ca">${ds.map(d=>`<option value="${d}" ${d===S.a?'selected':''}>${fd(d)}</option>`).join('')}</select></div>
 <div><label for="cb">Data final</label><select id="cb">${ds.map(d=>`<option value="${d}" ${d===S.b?'selected':''}>${fd(d)}</option>`).join('')}</select></div></div><div class="tbl" id="cmp"></div></div>`}`;
 document.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{S.metric=b.dataset.m;evolucao()});
 if(!rs.length)return;
 const cmp=()=>{S.a=$('#ca').value;S.b=$('#cb').value;
  const A=rs.find(r=>r.data===S.a),B=rs.find(r=>r.data===S.b);
  $('#cmp').innerHTML=`<table style="min-width:420px"><thead><tr><th>Item</th><th>${fd(S.a)}</th><th>${fd(S.b)}</th><th>Diferença</th></tr></thead><tbody>
  ${['peso',...M.map(m=>m[0])].map(x=>{const d=A[x]!=null&&B[x]!=null?B[x]-A[x]:null;
   return`<tr><td>${LBL[x]}</td><td>${nf(A[x])}</td><td>${nf(B[x])}</td><td class="${d>0?'up':d<0?'dn':''}">${d==null?'–':(d>0?'+':'')+nf(d)}</td></tr>`}).join('')}</tbody></table>`};
 $('#ca').onchange=$('#cb').onchange=cmp;cmp();
}

/* ---------- PERFIL ---------- */
function perfil(){
 const u=me();
 $('#main').innerHTML=`<h2>Perfil</h2><div class="card"><div class="f">
 <div><label for="pn">Nome</label><input id="pn" value="${esc(u.nome)}"><p class="err" id="e-pn"></p></div>
 <div><label for="pe">E-mail</label><input id="pe" type="email" value="${esc(u.email)}"><p class="err" id="e-pe"></p></div>
 <div><label for="pa">Altura (cm)</label><input id="pa" inputmode="decimal" value="${u.altura??''}"><p class="err" id="e-pa"></p></div>
 <div><label for="pd">Nascimento</label><input id="pd" type="date" max="${today()}" value="${u.nasc||''}"></div>
 <div class="full"><label for="ps">Nova senha (deixe em branco para manter)</label><input id="ps" type="password" autocomplete="new-password"><p class="err" id="e-ps"></p></div></div>
 <div class="row" style="margin-top:14px"><button class="btn" id="sp">Salvar perfil</button></div></div>
 <div class="card"><h3>Excluir conta</h3><p class="muted">Remove sua conta e todos os seus registros deste navegador.</p><button class="btn d" id="dx">Excluir minha conta</button></div>`;
 $('#sp').onclick=async()=>{
  ['pn','pe','pa','ps'].forEach(i=>fe(i));let ok=true;
  const nome=$('#pn').value.trim(),email=$('#pe').value.trim().toLowerCase(),a=num($('#pa').value),s=$('#ps').value;
  if(nome.length<2){fe('pn','Informe seu nome.');ok=false}
  if(!/^\S+@\S+\.\S+$/.test(email)){fe('pe','Informe um e-mail válido.');ok=false}
  else if(DB.users.some(x=>x.email===email&&x.id!==u.id)){fe('pe','Este e-mail já está em uso.');ok=false}
  if($('#pa').value.trim()!==''&&(isNaN(a)||a<80||a>250)){fe('pa','Informe uma altura entre 80 e 250.');ok=false}
  if(s&&s.length<6){fe('ps','A senha precisa ter ao menos 6 caracteres.');ok=false}
  if(!ok)return;
  u.nome=nome;u.email=email;u.altura=$('#pa').value.trim()===''?null:a;u.nasc=$('#pd').value;
  if(s){u.salt=uid()+uid();u.hash=await hash(s,u.salt)}
  save();toast('Perfil atualizado.');render();};
 $('#dx').onclick=function(){
  if(!this.dataset.c){this.dataset.c=1;this.textContent='Clique de novo para confirmar';return}
  DB.recs=DB.recs.filter(r=>r.uid!==u.id);DB.users=DB.users.filter(x=>x.id!==u.id);save();logout();};
}
(async()=>{
 try{
  const r=await fetch('/api/me');
  if(r.ok){const d=await r.json();sync(d.usuario);S.uid=d.usuario.id}
 }catch(e){}
 render();
})();
