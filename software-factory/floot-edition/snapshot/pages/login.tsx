import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { LockKeyhole, Layers3, ShieldCheck, ArrowLeft } from "lucide-react";
import { PasswordLoginForm } from "../components/PasswordLoginForm";
import { useAuth } from "../helpers/useAuth";
import styles from "./login.module.css";
export default function LoginPage() {
  const { authState } = useAuth();
  if (authState.type === "authenticated") return <Navigate to="/" replace/>;
  return <main className={styles.root}><div className={styles.panel}>
    <div className={styles.brand}><Layers3 size={25}/><span>TAP <b>STUDIO</b></span></div>
    <div className={styles.kicker}><ShieldCheck size={15}/> Acesso seguro · Floot Edition</div>
    <h1>Entre no seu workspace.</h1>
    <p>Projetos privados, código editável e informações persistentes. A versão Floot é independente do backend Python original.</p>
    <div className={styles.form}><PasswordLoginForm/></div>
    <p>Cadastro de novas contas temporariamente restrito. Acesso disponível às contas já autorizadas.</p>
    <div className={styles.note}><LockKeyhole size={15}/> Primeiro acesso do responsável: selecione <strong>Forgot password?</strong> e configure sua senha pelo e-mail cadastrado.</div>
    <div className={styles.foot}>MADE BY TAP · <a href="https://github.com/thalesandradepereira/tap-engineering-standard" target="_blank" rel="noopener noreferrer">CÓDIGO-FONTE GITHUB ↗</a></div>
  </div></main>;
}
