"use client";

import { useTransition } from "react";
import { useRouter } from "next/navigation";
import { signOut } from "@/app/actions";

export default function LogoutButton() {
  const router = useRouter();
  const [pending, startTransition] = useTransition();

  function onClick() {
    startTransition(async () => {
      await signOut();
      router.push("/login");
      router.refresh();
    });
  }

  return (
    <button className="btn btn--ghost" onClick={onClick} disabled={pending} style={{ padding: "10px 16px", fontSize: 14 }}>
      Log out
    </button>
  );
}
