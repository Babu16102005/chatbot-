import React, {useState} from 'react'
import axios from 'axios'
export default function MCQTest({token,me}){
  const [text,setText]=useState(''), [level,setLevel]=useState('basic'), [mcqs,setMcqs]=useState([]), [answers,setAnswers]=useState({})
  async function gen(e){ e.preventDefault()
    try{
      const r = await axios.post('http://localhost:8000/api/mcq/generate', {text, level}, {headers:{Authorization:`Bearer ${token}`}});
      setMcqs(r.data.mcqs)
    }catch(err){ alert('Generate failed') }
  }
  function selectAns(i, idx){
    setAnswers(prev=>({...prev, [i]: idx}))
  }
  async function submit(){
    // compute score
    let score = 0
    mcqs.forEach((m,i)=>{ if(answers[i]===m.answer) score += 1 })
    alert('Score: '+score+'/'+mcqs.length)
    // send progress update
    try{
      await axios.post('http://localhost:8000/api/progress/update', {user_id: me._id, delta_score: score, test_result:{score, total:mcqs.length, level}}, {headers:{Authorization:`Bearer ${token}`}})
    }catch(err){ console.log('progress update failed') }
  }
  return (
    <div className="card">
      <h4>MCQ Generator</h4>
      <form onSubmit={gen}>
        <textarea placeholder="Paste transcript or notes here" value={text} onChange={e=>setText(e.target.value)} style={{height:100}} />
        <div style={{display:'flex',gap:8,marginTop:8}}>
          <select value={level} onChange={e=>setLevel(e.target.value)}><option value="basic">Basic</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select>
          <button className="btn" type="submit">Generate MCQs</button>
        </div>
      </form>
      {mcqs.length>0 && <div style={{marginTop:12}}>{mcqs.map((m,i)=>(<div key={i} style={{marginBottom:12}}><div style={{fontWeight:700}}>{i+1}. {m.q}</div>{m.options.map((o,oi)=>(<div key={oi} style={{marginLeft:8}}><label><input type="radio" name={'q'+i} onChange={()=>selectAns(i, oi)} /> {o}</label></div>))}</div>))}<div style={{display:'flex',gap:8}}><button className="btn" onClick={submit}>Submit Test</button></div></div>}
    </div>
  )
}
