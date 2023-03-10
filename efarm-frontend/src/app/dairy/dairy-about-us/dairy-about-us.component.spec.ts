import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyAboutUsComponent } from './dairy-about-us.component';

describe('DairyAboutUsComponent', () => {
  let component: DairyAboutUsComponent;
  let fixture: ComponentFixture<DairyAboutUsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyAboutUsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyAboutUsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
