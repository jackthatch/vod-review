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
    <button
      onClick={onClick}
      disabled={pending}
      style={{ padding: "8px 14px", fontSize: 14, borderRadius: 6, cursor: "pointer" }}
    >
      Log out
    </button>
  );
}
