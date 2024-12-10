import React from 'react';
import { Button } from "../ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"
import { Input } from "../ui/input"
import { Label } from "../ui/label"

const SignInForm = () => (
  <div className="grid gap-4 py-4">
    <div className="grid gap-2">
      <Label htmlFor="email">Email</Label>
      <Input id="email" type="email" placeholder="Enter your email" />
    </div>
    <div className="grid gap-2">
      <Label htmlFor="password">Password</Label>
      <Input id="password" type="password" placeholder="Enter your password" />
    </div>
    <Button type="submit">Sign In</Button>
  </div>
);

const SignUpForm = () => (
  <div className="grid gap-4 py-4">
    <div className="grid gap-2">
      <Label htmlFor="name">Full Name</Label>
      <Input id="name" type="text" placeholder="Enter your name" />
    </div>
    <div className="grid gap-2">
      <Label htmlFor="email">Email</Label>
      <Input id="email" type="email" placeholder="Enter your email" />
    </div>
    <div className="grid gap-2">
      <Label htmlFor="password">Password</Label>
      <Input id="password" type="password" placeholder="Choose a password" />
    </div>
    <Button type="submit">Create Account</Button>
  </div>
);

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-white text-xl font-bold">AI Content Generator</h1>
        <div className="space-x-2">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="secondary">Login</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Sign In</DialogTitle>
                <DialogDescription>
                  Enter your credentials to access your account.
                </DialogDescription>
              </DialogHeader>
              <SignInForm />
            </DialogContent>
          </Dialog>
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline">Sign Up</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create Account</DialogTitle>
                <DialogDescription>
                  Fill in the details below to create your account.
                </DialogDescription>
              </DialogHeader>
              <SignUpForm />
            </DialogContent>
          </Dialog>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

