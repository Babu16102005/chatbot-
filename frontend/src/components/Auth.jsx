import React, {useState} from 'react'
import axios from 'axios'
export default function Auth({onLogin}){
  const [email,setEmail]=useState(''), [password,setPassword]=useState(''), [otp,setOtp]=useState(''), [step,setStep]=useState('register')
  async function register(e){ e.preventDefault()
    try{ await axios.post('http://localhost:8000/api/auth/register', {email,password}); alert('Registered. OTP sent (or printed in backend).'); setStep('verify') }
    catch(err){ alert(err?.response?.data?.detail || 'Register failed') }
  }
  async function verify(e){ e.preventDefault()
    try{ await axios.post('http://localhost:8000/api/auth/verify-otp', null, {params:{email,otp}}); alert('Verified. Please login.'); setStep('login') }
    catch(err){ alert(err?.response?.data?.detail || 'Verify failed') }
  }
  async function login(e){ e.preventDefault()
    try{ const r = await axios.post('http://localhost:8000/api/auth/login', {email,password}); onLogin(r.data.access_token) }
    catch(err){ alert(err?.response?.data?.detail || 'Login failed') }
  }
  return (
    <div className="card">
      {step==='register' && <form onSubmit={register}><h3>Create account</h3><input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} /><input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} style={{marginTop:8}}/><div style={{display:'flex',gap:8,marginTop:8}}><button className="btn" type="submit">Register</button><button type="button" className="btn" onClick={()=>setStep('login')} style={{background:'#ddd',color:'#111'}}>Have account? Login</button></div></form>}
      {step==='verify' && <form onSubmit={verify}><h3>Verify OTP</h3><input placeholder="OTP" value={otp} onChange={e=>setOtp(e.target.value)} /><div style={{marginTop:8}}><button className="btn" type="submit">Verify</button></div></form>}
      {step==='login' && <form onSubmit={login}><h3>Login</h3><input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} /><input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} style={{marginTop:8}}/><div style={{marginTop:8}}><button className="btn" type="submit">Login</button></div></form>}
    </div>
  )
}
