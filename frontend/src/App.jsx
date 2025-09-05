import React, {useState,useEffect} from 'react'
import Auth from './components/Auth'
import VideoSearch from './components/VideoSearch'
import MCQTest from './components/MCQTest'
import axios from 'axios'

export default function App(){
  const [token, setToken] = useState(localStorage.getItem('token')||null)
  const [me, setMe] = useState(null)

  useEffect(()=>{
    if(token){
      axios.get('http://localhost:8000/api/auth/me', {headers:{Authorization:`Bearer ${token}`}})
        .then(r=>setMe(r.data))
        .catch(()=>{ localStorage.removeItem('token'); setToken(null) })
    }
  },[token])

  return (
    <div className="container">
      <header className="app-header">
        <h1>Career ChatBot</h1>
        <div>
          {token ? <button className="btn" onClick={()=>{localStorage.removeItem('token'); setToken(null); setMe(null)}}>Logout</button> : null}
        </div>
      </header>

      {!token ? <Auth onLogin={(t)=>{localStorage.setItem('token', t); setToken(t)}} /> : (
        <>
          <div style={{display:'flex',gap:12}}>
            <div style={{flex:1}}>
              <VideoSearch token={token} />
            </div>
            <div style={{width:320}}>
              <MCQTest token={token} me={me} />
            </div>
          </div>
        </>
      )}
    </div>
  )
}
