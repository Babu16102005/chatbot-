import React, {useState} from 'react'
import axios from 'axios'
export default function VideoSearch({token}){
  const [query,setQuery]=useState(''), [results,setResults]=useState([]), [selected,setSelected]=useState(null)
  async function search(e){ e.preventDefault()
    try{
      const r = await axios.post('http://localhost:8000/api/videos/search', {query, lang:'en'}, {headers:{Authorization:`Bearer ${token}`}});
      setResults(r.data.results)
    }catch(err){ alert('Search error') }
  }
  async function summarize(url){
    try{
      const r = await axios.post('http://localhost:8000/api/videos/summarize', {video_url:url, topics:[]}, {headers:{Authorization:`Bearer ${token}`}});
      alert('Summary:\n'+r.data.summary.summary || r.data.summary)
    }catch(err){ alert('Summarize failed') }
  }
  return (
    <div>
      <div className="card">
        <form onSubmit={search} className="row">
          <input type="text" placeholder="Search e.g. Full Stack Development" value={query} onChange={e=>setQuery(e.target.value)} />
          <button className="btn" type="submit">Search</button>
        </form>
      </div>
      <div className="card">
        <h4>Results</h4>
        {results.length===0 && <div className="muted">No results</div>}
        {results.map((r,i)=>(<div key={i} className="result" onClick={()=>setSelected(r)}><div style={{fontWeight:700}}>{r.title}</div><div className="muted">{r.views} • {r.language}</div></div>))}
      </div>
      <div style={{marginTop:12}} className="card">
        {selected ? (<div><h4>{selected.title}</h4><div className="muted">{selected.views} • {selected.language}</div><div style={{marginTop:8}}><a href={selected.url} target="_blank" rel="noreferrer">Open in Brave / YouTube</a></div><div style={{marginTop:8}}><button className="btn" onClick={()=>summarize(selected.url)}>Summarize</button></div></div>) : <div className="muted">Select a video</div>}
      </div>
    </div>
  )
}
