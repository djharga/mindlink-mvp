import Head from 'next/head'
import {useState} from 'react'

export default function Home(){
  const [text, setText] = useState('')
  const [result, setResult] = useState('')

  async function handleSend(){
    const res = await fetch((process.env.NEXT_PUBLIC_API || '') + '/v1/generate', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({text, lang:'ar'})
    })
    const data = await res.json()
    setResult(data.result)
  }

  return (
    <div style={{padding:20, fontFamily:'Arial'}}>
      <Head><title>MindLink Web</title></Head>
      <main>
        <h1>MindLink — Web MVP</h1>
        <textarea value={text} onChange={e=>setText(e.target.value)} style={{width:'100%',height:120}} />
        <div style={{marginTop:10}}>
          <button onClick={handleSend}>تحويل</button>
        </div>
        <pre style={{whiteSpace:'pre-wrap', marginTop:20}}>{result}</pre>
      </main>
    </div>
  )
}
